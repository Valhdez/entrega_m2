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
    return [(True, dict_1, 'list_v1', pd.DataFrame(columns=["created", "task", "summary", "status", "owner"])),
            (False, dict_2, 'list_v2', pd.DataFrame(columns=["created", "task", "summary", "status", "owner"]))]

@pytest.mark.parametrize('Bool, new_reg, name_ls, df', obtener_datos_test_integration())
def test_add_to_list(Bool, new_reg, name_ls, df, df_full, tmp_dir):

    todos.create_list(name_ls)
    p_df = todos.load_list(name_ls)

    todos.add_to_list(name_ls, new_reg)
    s_df = todos.load_list(name_ls)

    assert ((len(pd.concat([p_df, df], axis=1).columns.unique())==5) and 
            (pd.concat([df_full,s_df],axis=0).drop_duplicates().shape[0]==1)) == Bool