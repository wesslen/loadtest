# loadtest/visualize_results.py
import streamlit as st
import pandas as pd
import altair as alt
import os
import typer

app = typer.Typer()


@app.command()
def visualize_data(
    data_dir: str = typer.Argument(
        "loadtest/data", help="The directory where the CSV files are stored."
    )
):
    """
    Launches a Streamlit app to visualize load test results from CSV files stored in a specified directory.
    """

    st.title("Load Test Results Visualization")

    if os.path.isdir(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    else:
        st.error(f"The specified directory {data_dir} does not exist.")
        st.stop()

    if not files:
        st.error("No CSV files found in the specified directory.")
        st.stop()

    # Dropdown to select the file
    selected_file = st.selectbox("Select a result file", files)

    # Load the selected file
    file_path = os.path.join(data_dir, selected_file)
    data = pd.read_csv(file_path)

    # Dropdown for Endpoint selection
    endpoint = st.selectbox("Select the endpoint", data["Endpoint"].unique())

    # Dropdowns for other user selections
    request_type = st.selectbox(
        "Select the type of request", data["Request Type"].unique()
    )
    y_axis = st.selectbox("Select Y-axis metric", ["Average Duration", "Duration", "Failures"])

    # Filter data based on the selected request type and endpoint
    filtered_data = data[
        (data["Request Type"] == request_type) & (data["Endpoint"] == endpoint)
    ]

    if y_axis == "Average Duration" or y_axis == "Duration":
        # Calculate average duration if needed
        filtered_data["Average Duration"] = filtered_data["Duration"] / filtered_data["Concurrency"]
        if y_axis == "Average Duration":
            y_axis_value = "Average Duration"
        else:
            y_axis_value = "Duration"
    else:
        y_axis_value = y_axis

    # Generate and display the Altair chart
    st.markdown("### Results")
    chart = (
        alt.Chart(filtered_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("Concurrency:Q", title="Concurrency"),
            y=alt.Y(f"{y_axis_value}:Q", title=y_axis_value),
            color=alt.Color("Payload Size:N", title="Payload Size"),
            tooltip=[
                alt.Tooltip("Endpoint:N", title="Endpoint"),
                alt.Tooltip("Request Type:N", title="Request Type"),
                alt.Tooltip("Concurrency:Q", title="Concurrency"),
                alt.Tooltip(f"{y_axis_value}:Q", title=y_axis_value),
                alt.Tooltip("Payload Size:N", title="Payload Size"),
            ],
        )
        .properties(width=700, height=300)
    )

    st.altair_chart(chart)

    # Display the data table below the chart
    st.markdown("### Detailed Data Table")
    if y_axis_value != "Duration":  # Show Average Duration in the table if selected
        display_columns = ["Endpoint", "Request Type", "Payload Size", "Concurrency", y_axis_value]
    else:
        display_columns = ["Endpoint", "Request Type", "Payload Size", "Concurrency", "Duration"]
    st.write(filtered_data[display_columns])


if __name__ == "__main__":
    app()
