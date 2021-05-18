import os

list_folder = "C:\\Users\\there\\Desktop\\file_list"
output_filename = "missing_files.txt"

clean_url_list = []
clean_file_list = []

missing_urls = []

with open(os.path.join(list_folder, "subset_M2I3NVASM_5.12.4_20210317_162050.txt")) as f:
	url_list = f.read()

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