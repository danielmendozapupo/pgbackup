import tempfile
import pytest

from pgbackup import storage

@pytest.fixture
def infile():
    f = tempfile.TemporaryFile('r+b')
    f.write(b"Testing")
    f.seek(0)
    return f

def test_storing_file_locally(infile):
    """
    Write content from one file to another
    """
    outfile = tempfile.NamedTemporaryFile(delete=False)
    storage.local(infile, outfile)
    with open(outfile.name,'rb') as f:
        assert f.read() == b"Testing"

def test_storing_file_on_s3(mocker, infile):
    """
    Writes content from one file-like to S3
    """
    client = mocker.Mock()
    storage.s3(client, infile,"bucket","file-name")
    client.upload_fileobj_assert_called_with(infile,"bucket", "file_name")

