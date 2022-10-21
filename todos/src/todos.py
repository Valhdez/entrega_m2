import os
from numpy import str_
import typer
import pandas as pd
from datetime import datetime
from pathlib import Path

#PATH_TO_DATA = "todos/data/"
PATH_TO_DATA = "C:/Users/hdezv/OneDrive/Documentos/GitHub/entrega_m2/todos/data/"

app = typer.Typer(add_completion=False)


@app.command("create")
def create(name: str = typer.Option("Unnamed", "-ln", "--listname")):

    """Create a new todo list

    Parameters
    ----------
    name: str name
    Returns
    "File_Name.csv"
    """

    if check_list_exists(name):
        print("There is already a todo list with this name.")
        return

    create_list(name)
    print(f"Todo list {name} successfully created!")


@app.command("list")
def list_lists():
    """
    List of the all list
    Returns
    list of files stored
    """

    existing_lists = get_existing_lists()
    for ls in existing_lists:
        print(ls)


@app.command("show")
def show_list(list_name: str = typer.Option(..., "-ln", "--listname")):
    """Shows Task in one list

    Parameters
    ----------
    list_name: name in string
    Returns
    Get the list if the list exist, if not, get a string
    """
    if not check_list_exists(list_name):
        print("The list does not exist. Use create list first.")
        return
    df = load_list(list_name)
    print(df.to_markdown())


@app.command("add")
def add_task(
    list_name: str = typer.Option(..., "-ln", "--listname"),
    task_name: str = typer.Option(..., "-tn", "--taskame"),
    summary: str = typer.Option(None, "-d", "--description"),
    owner: str = typer.Option(..., "-o", "--owner"),
):
    """Add a task to a given todo list

    Parameters
    ----------
    list_name: name in string
    task_name: name of task string
    summary: description of task in string
    owner: ownershiop in string
    Returns
    Add a task to the previous list
    """

    if not check_list_exists(list_name):
        print("The list does not exist. Use create list first.")
        return

    new_row = {
        "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "task": task_name,
        "summary": summary if summary else None,
        "status": "todo",
        "owner": owner,
    }

    add_to_list(list_name, new_row)
    print("Task successfully added")


@app.command("update")
def update_task(
    list_name: str = typer.Option(..., "-ln", "--listname"),
    task_id: int = typer.Option(..., "-i", "--taskid"),
    field: str = typer.Option(..., "-f", "--field"),
    change: str = typer.Option(..., "-c", "--change"),
):

    """Update a task in a given todo list

    Parameters
        list_name: name in string
        task_id: Index
        field: Name of column
        change: change to realize
    """
    if not check_list_exists(list_name):
        print("The list does not exist. Use create list first.")
        return
    update_task_in_list(list_name, task_id, field, change)
    print("Task successfully updated")


def update_task_in_list(
    list_name: str, 
    task_id: str, 
    field: str, 
    change: str
):
    """
    Update the values in a selected index
    Parameters
        list_name : string name
        task_id : Index
        field : Column
        change : The Value that will be changed
    """
    df = load_list(list_name)
    df.loc[task_id, field] = change
    store_list(df, list_name)


def create_list(name: str):
    """

    Add a new a new list

    Parameters
    name : String Name
    Returns
    DataFrame
    """
    df = pd.DataFrame(columns=["created",
                               "task",
                               "summary",
                               "status",
                               "owner"])
    store_list(df, name)


def get_existing_lists():
    """
    check if the list was exist

    Parameters
        name : string
    Returns
        PATH_TO_DATA
    """
    return os.listdir(PATH_TO_DATA)


def check_list_exists(name: str):

    """
    check if the list was created
    Parameters
    name :
        string
    Returns
        boolean
    """
    return get_list_filename(name) in get_existing_lists()


def get_list_filename(name: str):
    """
    Get the name of file
    Parameters
    name :
        string
    Returns
        string
    """
    return f"{name}.csv"


def load_list(name: str):
    """
    Load the File
    Parameters
    name : string of name
    Returns:
        DataFrame
    """
    return pd.read_csv(get_list_path(name))


def store_list(
    df: pd.DataFrame,
    name: str
):
    """
    Save a new list
    Parameters
        df : DataFrame
        name : str name
    """
    df.to_csv(get_list_path(name), index=False)


def get_list_path(name: str):
    """
    Return te path of file were stored

    Parameters
        name : str name
    Returns
        string
    """
    return f"{PATH_TO_DATA}{get_list_filename(name)}"


def add_to_list(list_name: str, new_row):
    """
    Add the news values and save the file
    Parameters
        list_name : name in string
        new_row : dictionary with news Values
    """
    df = load_list(list_name)
    df.loc[len(df.index)] = new_row
    store_list(df, list_name)


if __name__ == "__main__":
    create('Intento_1')
