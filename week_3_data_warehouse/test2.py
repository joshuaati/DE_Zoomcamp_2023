import gcsfs
import pyarrow.parquet as pq
from gcsfs import GCSFileSystem
import os

path_ = '/Users/emmanuel.ogunwede/Downloads/josh-shared-sa.json'
file_ = 'dagster-proj/api-response.parquet'
project_id = 'infinite-rider-376814'

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/Users/emmanuel.ogunwede/Downloads/josh-shared-sa.json'

class GCSParquetToDataframe:
    def _init_(self, project_id:str, token_path:str=None) -> None:
        """
        convert parquet files on GCS into pandas dataframe

        whatever asset that attempts to use the GCSParquetToDataframe resource would 
        have to provide the project_id and optionally the token_path under variables
        of StringSourceType

        Parameters
        ----------
        project_id: string
            project_id to work under. This is required by gcfs in order
            to list all the buckets you have access to within a project and to
            create/delete buckets
        token_path: string
            while gcsfs has a vairety of options for authentication and is capable
            of implicitly autheticating by trying to find your default credentials,
            one of the easiet way of autheticating is by providing the path to a json
            file for authetication and token_path allows you to explicitly pass that path.
            
        """
        self.token_path = token_path
        self._project = project_id
        self.fs = None
    
    
    def _get_file_system(self):
        if not self.token_path:
            self.token_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)
        
        # when the token is none gcsfs will try to find your default credential and use it to access gcs
        return gcsfs.GCSFileSystem(project=self._project, token=self.token_path)
    
    def fetch_from_gcs(self, gcs_filepath):
        # the file path is the full path to the object e.g bukcet/prefix/key
        # where key is the name of the file e.g example.parquet
        if not self.fs:
            self.fs = self._get_file_system()
        
        pf = pq.ParquetDataset(gcs_filepath,filesystem=self.fs)
        return pf.read_pandas().to_pandas()


handler = GCSParquetToDataframe(project_id=project_id, token_path=path_)

df = handler.fetch_from_gcs(gcs_filepath=file_)

print(df.head())