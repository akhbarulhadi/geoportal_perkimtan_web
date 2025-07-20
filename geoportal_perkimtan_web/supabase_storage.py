from django.core.files.storage import Storage
from django.conf import settings
import mimetypes

class SupabaseStorage(Storage):
    def __init__(self, client=None, bucket_name=None):
        self.client = client or settings.SUPABASE_CLIENT
        self.bucket_name = bucket_name or settings.SUPABASE_BUCKET_NAME

    def _get_bucket(self):
        return self.client.storage.from_(self.bucket_name)

    def _save(self, name, content):
        # Pastikan nama file menggunakan / sebagai pemisah folder
        name = name.replace("\\", "/")
        print(f"Saving file to {name}")  # Debug untuk memastikan nama file
        bucket = self._get_bucket()
        content.seek(0)
        mimetype, _ = mimetypes.guess_type(name)

        # Upload file ke bucket Supabase
        result = bucket.upload(name, content.read(), {"content-type": mimetype or "application/octet-stream"})

        # Debug: print hasil result upload
        print(f"Upload result: {result}")

        # Validasi hasil upload berdasarkan atribut 'path'
        if hasattr(result, 'path') and result.path == name:
            return name
        else:
            # Jika upload gagal, tangani error dengan benar
            error_message = getattr(result, 'error', 'Unknown error')
            print(f"Error details: {result}")  # Debug untuk melihat detail error
            raise Exception(f"Upload failed: {error_message}")


    def url(self, name):
        name = name.replace("\\", "/")  # Pastikan url menggunakan /
        # print(f"Generating signed URL for: {name}")  # Debugging nama file
        bucket = self._get_bucket()
        result = bucket.create_signed_url(name, expires_in=3600)
        # print(f"Result from Supabase: {result}")  # Debugging hasil response
    
        # Periksa apakah signed URL berhasil dibuat
        if result and 'signedURL' in result:
            return result['signedURL']
        else:
            print(f"Failed to generate signed URL. Result: {result}")  # Debug jika URL gagal dibuat
            raise Exception(f"Failed to generate signed URL: {result.get('message', 'Unknown error')}")
        

    def exists(self, name):
        name = name.replace("\\", "/")  # Pastikan pengecekan menggunakan /
        bucket = self._get_bucket()
        try:
            bucket.download(name)
            return True
        except Exception as e:
            if 'not found' in str(e).lower():
                return False
            raise e
