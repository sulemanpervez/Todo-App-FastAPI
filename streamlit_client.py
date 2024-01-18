import streamlit as st
import pandas as pd
import requests

# Todo Already Exist Function
def todo_exists(todo_id):
    # Function to check if todo with given ID already exists
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    return response.status_code == 200

BASE_URL = "http://127.0.0.1:8000"

def create_todo():
    st.subheader("Add Items")

    # Layout
    # Creating a Two Column to Show the id, title, and description
    col1, col2 = st.columns(2)
    with col1:
        id = st.text_input("Enter Todo ID")
        title = st.text_area("Enter Todo Title") 

    with col2:
        description = st.text_area("Enter Todo Description")

    # if Todo not in Database to Add the Todo but if Todo have in Database to show the Error Todo id Already Exits
    if st.button("Add Todo"):
        if not todo_exists(id):
            response = requests.post(f"{BASE_URL}/todos", json={"id": id, "title": title, "description": description})
            if response.status_code == 200:
                st.success(f"Added Todo Successfully")
            else:
                st.error(f"Todo with ID {id} already exists!")

def read_todos():
    st.subheader("View Items")
    response = requests.get(f"{BASE_URL}/todos/")
    df = pd.DataFrame(response.json(), columns=["id", "title", "description"])
    with st.expander("View All Data"):
        st.dataframe(df)

def update_todo():
    st.subheader("Edit/Update Items")

    # Fetch the list of todos
    response = requests.get(f"{BASE_URL}/todos/")
    todos = response.json()

    # Display current todos
    df = pd.DataFrame(todos, columns=["id", "title", "description"])
    with st.expander("Current Data"):
        st.dataframe(df)

    # Get the titles of existing todos
    list_of_todo_titles = [todo['title'] for todo in todos]

    # Select the todo to edit
    selected_todo_title = st.selectbox("Todo to Edit", list_of_todo_titles)

    # Find the selected todo by title
    selected_todo = next((todo for todo in todos if todo['title'] == selected_todo_title), None)

    if selected_todo:
        # Display details of the selected todo
        st.write(selected_todo)
        todo_id = selected_todo['id']
        title = selected_todo['title']
        description = selected_todo['description']

        # Layout
        col1, col2 = st.columns(2)

        with col1:
            # Display the existing ID but don't allow changes
            st.text("Todo ID")
            new_id = st.text_input("Todo ID", todo_id)

        # Allow the user to update other fields
        new_title = st.text_area("Enter Todo Title", title)

        with col2:
            new_description = st.text_area("Enter Todo Description", description)

        if st.button("Update Todo"):
            response = requests.put(f"{BASE_URL}/todos/{todo_id}", json={"id": new_id, "title": new_title, "description": new_description})
            if response.status_code == 200:
                st.success(f"Todo with ID {todo_id} updated successfully")
            elif response.status_code == 404:
                st.warning(f"Todo with ID {todo_id} not found")
            else:
                st.error(f"Failed to update Todo with ID {todo_id}. Status Code: {response.status_code}, Response Text: {response.text}")

    # Fetch the list of todos
    response2 = requests.get(f"{BASE_URL}/todos/")
    todos = response2.json()

    # Display current todos
    df2 = pd.DataFrame(todos, columns=["id", "title", "description"])
    with st.expander("Updated Data"):
        st.dataframe(df2)

def delete_todo():
    st.subheader("Delete Items")
    # Fetch the list of todos
    response = requests.get(f"{BASE_URL}/todos/")
    todos = response.json()

    # Display current todos
    df = pd.DataFrame(todos, columns=["id", "title", "description"])
    with st.expander("Current Data"):
        st.dataframe(df)
    todo_id = st.text_input("Enter Todo ID to Delete")
    st.warning(f"Do You want to Delete Selected Id {todo_id}")
    if st.button("Delete Todo"):
        response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
        if response.status_code == 200:
            st.success(f"Todo with ID {todo_id} deleted successfully")
        elif response.status_code == 404:
            st.warning(f"Todo with ID {todo_id} not found")
        else:
            st.error(f"Failed to delete Todo with ID {todo_id}")

    response2 = requests.get(f"{BASE_URL}/todos/")
    todos = response2.json()

    # Display current todos
    df2 = pd.DataFrame(todos, columns=["id", "title", "description"])
    with st.expander("Updated Data"):
        st.dataframe(df2)

def about_app():
    st.subheader("About")

def main():
    st.title("Todo App")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Create", "Read", "Update", "Delete", "About"])

    with tab1:
        create_todo()
    with tab2:
        read_todos()
    with tab3:
        update_todo()
    with tab4:
        delete_todo()
    with tab5:
        about_app()



if __name__ == "__main__":
    main()
