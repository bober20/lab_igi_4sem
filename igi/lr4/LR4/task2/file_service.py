import zipfile


class FileService:
    def read_text_from_file(self, file_path="lr_files/text.txt"):
        """This function reads text from file."""

        with open(file_path, 'r') as file:
            text_from_file = file.read()

        return text_from_file


    def write_results_to_file(self, result, file_path="lr_files/result.txt"):
        """This function writes text in file."""

        with open(file_path, 'w') as file:

            for i in result:
                file.write(str(i))


    def make_zip(self, file_path="lr_files/result.txt"):
        """This function makes zip files."""

        with zipfile.ZipFile('lr_files/lr4.zip', mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_path, arcname='result')


    def unzip(self):
        """This function unzips a zip."""

        with zipfile.ZipFile('lr_files/lr4.zip', mode='r') as zf:
            zf.extractall(path='lr_files/unziped')


    def get_inner_files_info(self):
        """This function returns info about file from zip."""

        with zipfile.ZipFile('lr_files/lr4.zip', mode='r') as zf:
            for file in zf.infolist():
                print(f"File name: {file.filename}, Date: {file.date_time}, Size: {file.file_size}")

