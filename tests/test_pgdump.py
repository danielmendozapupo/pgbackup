import pytest
import subprocess

from pgbackup import pgdump

url = "postgres://bob:password@example.com:5432/db_one"

def test_dump_calls_pg_dump(mocker):
    """
    Utilize pg_dump with the database URL
    """
    mocker.patch('subprocess.Popen')
    assert pgdump.dump(url)
    subprocess.Popen.assert_called_with(['pg_dump', url], stdout = subprocess.PIPE)


def test_dump_calls_pg_dump(mocker):
    """
    pgdump.dump returns a reasonable error if pg_dump isn't installed
    """
    mocker.patch('subprocess.Popen', side_effect=OSError('no such file'))
    with pytest.raises(SystemExit):
        pgdump.dump(url)

def test_dump_file_name_without_timestamp():
    """
    pgdump.dump-filename returns the name of the database
    """
    assert pgdump.dump_file_name(url) == "db_one.sql"


def test_dump_file_name_without_timestamp():
      """
      pgdump.dump-filename returns the name of the database with timestamp
      """
      timestamp = "2020-06-09T18:15:00"
      assert pgdump.dump_file_name(url,timestamp) == f"db_one-{timestamp}.sql"




