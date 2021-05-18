import os

list_folder = "/glade/scratch/kdagon/MERRA-2/3Dfields/3hrly_average/"
url_filename = "subset_M2T3NVASM_5.12.4_20210317_163623.txt"
output_filename = "missing_files.txt"

clean_url_list = []
clean_file_list = []

missing_urls = []

with open(os.path.join(list_folder, url_filename)) as f:
	url_list = f.read()

# filelist.txt created by piping all current .nc files to a txt file
# printf "%s\n" *.nc4 > filelist.txt
with open(os.path.join(list_folder, "filelist.txt")) as f:
	file_list = f.read()

for line in url_list.split("\n"):
	clean_url_list.append(line)

for line in file_list.split("\n"):
	clean_file_list.append(line)


for url in clean_url_list:
	found_flag = False
	
	for filename in clean_file_list:
		clean_url = url.split("?")[0].split("/")[-1]

		if filename == clean_url:
			found_flag = True
			break

	if found_flag:
		continue

	missing_urls.append(url)

with open(os.path.join(list_folder, output_filename), "w") as f:
	for url in missing_urls:
		f.write("%s\n" % (url, ))
# note: might need to manually remove README pdf from this file
