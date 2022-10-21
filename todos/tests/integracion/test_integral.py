import os
import sys
import pandas as pd
import pytest
import shutil
from datetime import datetime
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../..'))
from src import todos

@pytest.fixture(scope="function")
def tmp_dir(tmpdir_factory):
    my_tmpdir = tmpdir_factory.mktemp("pytestdata")
    todos.PATH_TO_DATA = my_tmpdir
    yield my_tmpdir
    shutil.rmtree(str(my_tmpdir))


@pytest.fixture(scope="function")
def new_row():
    return {
        "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "task": "cocinar",
        "summary": "Cocinar algo rico",
        "status": "todo",
        "owner": "Andre",
    }


@pytest.fixture(scope="function")
def df_full(new_row):
    return pd.DataFrame(
        [new_row], columns=["created", "task", "summary", "status", "owner"]
    )

dict_1 = {
        "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "task": "cocinar",
        "summary": "Cocinar algo rico",
        "status": "todo",
        "owner": "Andre",
    }

dict_2 = {
        "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "task": "Cocinar",
        "summary": "Como mi mama",
        "status": "sin talento",
        "owner": "@ValHdez",
    }


def obtener_datos_test_integration():
    return [(False, dict_1, 'list_v1', pd.DataFrame(columns=["created", "task", "summary", "status", "owner"])),
            (True, dict_2, 'list_v2', pd.DataFrame(columns=["created", "task", "summary", "status", "owner"]))]

@pytest.mark.parametrize('Bool, nr, tl, dataframe', obtener_datos_test_integration())
def test_add_to_list(Bool, nr, tl, dataframe, df_full, tmp_dir):

    todos.create_list(tl)
    df0 = todos.load_list(tl)
    d0 = (pd.concat([df0, dataframe], axis=1).columns.unique().shape[0]==5)

    todos.add_to_list(tl, nr)
    df1 = todos.load_list(tl)
    d1 = (df_full.append(df1).drop_duplicates().shape[0]>1)
    
    assert (d0 and d1)==Bool