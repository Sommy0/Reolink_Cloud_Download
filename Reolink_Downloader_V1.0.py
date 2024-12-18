from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from csv import reader, writer
import csv
import os
import shutil


def read_mp4_filenames(folder_path):
    mp4_files = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".mp4"):
            mp4_files.append(filename)
    return mp4_files

def truncate_filename(filename):
    truncated_name = filename[0:-30]
    return truncated_name

def create_directory(directory_path, directory_name):
    target_path = os.path.join(directory_path, directory_name)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    return target_path

def move_mp4_files(mp4_files, target_directory):
    for filename in mp4_files:
        source_path = os.path.join(folder_path, filename)
        target_name = truncate_filename(filename)  # shortet file name as folder name
        target_path = create_directory(target_directory, target_name)
        
        # check if file is already present in target path
        if os.path.exists(os.path.join(target_path, filename)):
            # if present, overwrite
            print(f"File present: {filename} to {target_path}")
        else:
            # If not, move file
            shutil.move(os.path.join(source_path), os.path.join(target_path))
            print(f"moved: {filename} to {target_path}")

def rename_files(folder_path):
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            # Get file name without filetype
            base_name, extension = os.path.splitext(filename)
            
            # Cut Filename
            new_name = base_name[-19:] + "_" + base_name[:-20] + extension
            
            # Alter Path
            source_path = os.path.join(folder_path, filename)
            target_path = os.path.join(folder_path, new_name)
            
            # Rename File
            os.rename(source_path, target_path)
            print(f"Umbenannt: {filename} -> {new_name}")



videos = []
videos_filtered = []
videos_downloaded = []

driver = webdriver.Chrome()
driver.maximize_window()
driver.headless = True


#---------------------------!!!!!!!Fill with your Information!!!!!!!-------------------------------------------------
Path_csv_videos = "C:\\Users\\YOUR_USERNAME\\Desktop\\Reolink_Downloader\\videos.csv"
Path_csv_videos_downloaded = "C:\\Users\\YOUR_USERNAME\\Desktop\\Reolink_Downloader\\videos_downloaded.csv"
Path_csv_videos_notdownloaded = "C:\\Users\\YOUR_USERNAME\\Desktop\\Reolink_Downloader\\videos_notdownloaded.csv"
Path_download_folder = "C:\\Users\\YOUR_USERNAME\\Downloads"
Path_videos_target = "C:\\Users\\YOUR_USERNAME\\Downloads\\Reolink" 
#--------------------------------------------------------------------------------------------------------------------


driver.get('https://my.reolink.com/login/')
email = driver.find_element(By.ID, 'email')
email.send_keys('YOUR_EMAIL') #!!!!!!!Fill with your Information!!!!!!!
#element.submit()
password = driver.find_element(By.ID, 'password')
password.send_keys('YOUR_PASSWORD')#!!!!!!!Fill with your Information!!!!!!!

driver.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div/div/div/div/div[1]/button').click()

time.sleep(5)

driver.get('https://cloud.reolink.com/user/cloud-library/')

time.sleep(5)

#Accept Cookies
driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/a[2]').click()

time.sleep(5)

nextbutton = True

while nextbutton:
 #searchses for all "class=cover" elements, to get the Video Link
 links = driver.find_elements(By.CLASS_NAME,'cover')
 #gets videos from the page and writes them to the videos list
 for link in links:
    videos.append(link.get_attribute('href'))
 #Go to next Page
 element = driver.find_element(By.CLASS_NAME,'pagination-forward')
 driver.find_element(By.CLASS_NAME,'pagination-forward').click()
 nextbutton = element.is_enabled() 

 time.sleep(10)   


#Filter video list to get rid of the "None" Datasets
for video in videos:
    if video is not None:
        videos_filtered.append(video)

# print("_________________________________________________________________________________________________")
# #print(videos_filtered)

#opens videos.csv and adds all video links from the videos_filtered list
with open(Path_csv_videos, 'w', encoding='utf-8-sig') as f: 
    writer = csv.writer(f, delimiter=',',lineterminator='\n')
    for row in videos_filtered:
     writer.writerow([row])

print("Writing to videos.csv done!")

#Compares already downloaded videos (videos_downloaded.csv) to the videos.csv the differences will be written to the "Videos_NotDownloaded.csv"
with open(Path_csv_videos_downloaded, 'r', encoding='utf-8-sig') as t1, open(Path_csv_videos, 'r', encoding='utf-8-sig') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

with open(Path_csv_videos_notdownloaded, 'w', encoding='utf-8-sig') as outFile:
    for line in filetwo:
        if line not in fileone:
            outFile.write(line)

print("Compare videos_downloaded.csv to videos.csv done!")

#Opens the Video Links from the videos_notdownloaded.csv and downloads them
#Additionaly the link of the downloaded video will be written to the videos_downloaded list
with open(Path_csv_videos_notdownloaded, mode ='r',  encoding='utf-8-sig')as file:
  urls = thereader = reader(file)
  for url in urls:
      print(url[0])
      driver.get(url[0])
      time.sleep(10)
      driver.find_element(By.XPATH,'//*[@id="player"]/section/main/div[1]/div[2]/ul/ul/div[1]/button').click()
      print("Heruntergeladen")
      videos_downloaded.append(url[0])
      time.sleep(10)

#Wries the Video links from the video_downloaded list to the videos_downloaded.csv
with open(Path_csv_videos_downloaded, 'a', encoding='utf-8-sig') as f: 
    writer = csv.writer(f, delimiter=',',lineterminator='\n')
    for row in videos_downloaded:
     writer.writerow([row])



#Sorts downloaded videos into folders named by YYYY-MM-DD
if __name__ == "__main__":
    folder_path = Path_download_folder  # Download folder Temp
    target_directory = Path_videos_target  # Target Path for sortet Videos

    rename_files(folder_path)

    mp4_filenames = read_mp4_filenames(folder_path)
    truncated_names = [truncate_filename(name) for name in mp4_filenames]

    for name in truncated_names:
        create_directory(target_directory, name)

    move_mp4_files(mp4_filenames, target_directory)


#clears the videos.csv
filename = Path_csv_videos
# opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()

#clears the videos_notdownloaded.csv
filename = Path_csv_videos_notdownloaded
# opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()

#time.sleep(100)
driver.quit()
