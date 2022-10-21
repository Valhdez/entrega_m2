import os
import sys
import pandas as pd
import pytest
import shutil
from datetime import datetime
sys.path.append( os.path.abspath(os.path.dirname(__file__)+'/../..') )
from src import todos

@pytest.fixture(scope="function")
def tmp_dir(tmpdir_factory):
    my_tmpdir = tmpdir_factory.mktemp("pytestdata")
    todos.PATH_TO_DATA = my_tmpdir
    yield my_tmpdir
    shutil.rmtree(str(my_tmpdir))


def data_to_dfs():
    return [(True, pd.DataFrame(columns=["created", "task", "summary", "status", "owner"])), 
            (False, pd.DataFrame(columns=["hour_create", "task", "description", "status", "who?"])),
            (False, pd.DataFrame(columns=["when", "what", "how", "stat", "who"]))
            ]

@pytest.mark.parametrize('Bool, df', data_to_dfs())
def test_create_list(tmp_dir, Bool, df):
    todos.create_list("todos")
    df1 = todos.load_list("todos")
    #assert (pd.concat([df1, dataframe], axis=1).columns.unique().shape[0]>5)==Bool
    assert (len(pd.concat([df1, df], axis=1).columns.unique())==5)==Bool