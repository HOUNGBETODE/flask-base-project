import os
import time
import shutil
from werkzeug.utils import secure_filename
from commons.instances.instances import logger
from commons.config.config.config import Config


class FileUploadManager:
    
    @staticmethod
    def upload_one_file(file, upload_file_path):
        try:
            filename = f"{int(time.time() * 1000)}_{secure_filename(file.filename)}"
            file_url = f"{upload_file_path}/{filename}"
            file_size = 0
            file_path = os.path.join(upload_file_path, filename)
            
            if not os.path.exists(file_path):
                file.save(file_path)
                file_size = os.path.getsize(file_url)
            
            return True, file_url, file_size
        except Exception as e:
            logger.error(f"Error in upload_one_file function utils: {e}")
            raise e
    

    @staticmethod
    def upload_multiple_files(files, upload_file_path):
        try:
            file_urls = []
            file_sizes = 0

            for file in files:
                filename = f"{int(time.time() * 1000)}_{secure_filename(file.filename)}"
                file_url = f"{upload_file_path}/{filename}"
                file_path = os.path.join(upload_file_path, filename)
                
                if not os.path.exists(file_path):
                    file.save(file_path)
                    file_sizes += os.path.getsize(file_url)

                file_urls.append({"file_name": filename, "file_path": file_url, "views_count": 0})
            return True, file_urls, file_sizes
        except Exception as e:
            logger.error(f"Error in upload_multiple_files function utils: {e}")
            raise e
    

    @staticmethod
    def delete_one_file(file_path) -> tuple[bool, int]:
        try:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                os.remove(file_path)
                return True, file_size
            return False, 0
        except Exception as e:
            logger.error(f"Error in delete_one_file function utils: {e}")
            raise e
    
    
    @staticmethod
    def delete_one_attachment_file(file_path) -> str | bool:
        try:
            if os.path.exists(file_path):
                destination = f"{Config.DELETED_ATTACHMENTS}/{os.path.basename(file_path)}"
                shutil.move(file_path, Config.DELETED_ATTACHMENTS)
                return destination
            return False
        except Exception as e:
            logger.error(f"Error in delete_one_attachment_file function utils : {e}")
            raise e
    
    
    @staticmethod
    def restore_one_attachment_file(file_path) -> str | bool:
        try:
            if os.path.exists(file_path):
                destination = f"{Config.UPLOAD_ATTACHMENT}/{os.path.basename(file_path)}"
                shutil.move(file_path, Config.UPLOAD_ATTACHMENT)
                return destination
            return False
        except Exception as e:
            logger.error(f"Error in restore_one_attachment_file function utils : {e}")
            raise e


    @staticmethod
    def delete_post_media_s(file_path_s) -> str | list:
        try:
            new_paths = []
            file_sizes = 0
            for file_dict in file_path_s:
                file_path = file_dict["file_path"]
                if os.path.exists(file_path):
                    basename = os.path.basename(file_path)
                    destination = f"{Config.DELETED_POST_MEDIAS}/{basename}"
                    shutil.move(file_path, Config.DELETED_POST_MEDIAS)
                    new_paths.append({"file_name": basename, "file_path": destination})
                    file_sizes += os.path.getsize(destination)
            return new_paths, file_sizes
        except Exception as e:
            logger.error(f"Error in delete_post_media_s function utils : {e}")
            raise e
    
    
    @staticmethod
    def restore_post_media_s(file_path_s) -> str | list:
        try:
            new_paths = []
            file_sizes = 0
            for file_dict in file_path_s:
                file_path = file_dict["file_path"]
                if os.path.exists(file_path):
                    basename = os.path.basename(file_path)
                    destination = f"{Config.UPLOAD_STAND_POST_MEDIA}/{basename}"
                    shutil.move(file_path, Config.UPLOAD_STAND_POST_MEDIA)
                    new_paths.append({"file_name": basename, "file_path": destination})
                    file_sizes += os.path.getsize(destination)
            return new_paths, file_sizes
        except Exception as e:
            logger.error(f"Error in restore_post_media_s function utils : {e}")
            raise e
