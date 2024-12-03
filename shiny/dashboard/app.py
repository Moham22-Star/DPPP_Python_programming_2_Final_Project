from shiny import App, render, ui
import pandas as pd
import altair as alt

# Loading and processing data
def load_data():
    data = pd.read_csv(
        "C:/Users/mmmoh/DPPS Python/PSet/DPPP_Python_programming_2_Final_Project/shiny/dashboard/somalia_energy_with_technology.csv"
    )
    data['Electricity Generation (TWh)'] = data['Electricity Generation (GWh)'].apply(
        lambda x: float(x) / 1000 if x != 'NA' else None
    )
    data['Primary energy consumption (TWh)'] = pd.to_numeric(
        data['Primary energy consumption (TWh)'], errors='coerce'
    )
    data['Technology'] = data['Technology'].fillna('Others')
    return data


# Loading data
data = load_data()

# Defining the UI
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider(
            "year_range", "Year Range", min=2000, max=2021, value=[2000, 2021]
        ),
        ui.input_select(
            "chart_type", "Chart Type", choices=["Line"]
        ),
        ui.input_checkbox_group(
            "technologies",
            "Select Technologies",
            choices=["Geothermal energy", "Marine energy", "Multiple renewables*", "Oil", "Onshore wind energy","Renewable hydropower", "Solar energy", "Wind energy","Solar photovoltaic", "Solar thermal energy",
        "Solid biofuels"],
            selected=["Geothermal energy", "Marine energy", "Multiple renewables*", "Oil", "Onshore wind energy","Renewable hydropower", "Solar energy", "Wind energy","Solar photovoltaic", "Solar thermal energy",
        "Solid biofuels"],
        ),
    ),
    ui.output_ui("dashboard"),
)

# Defining server logic
def server(input, output, session):
    @output
    @render.ui
    def dashboard():
        return ui.div(
            ui.h2("Somalia Energy Analysis Dashboard"),
            ui.h3(
                f"Energy Metrics from {input.year_range()[0]} to {input.year_range()[1]}"
            ),
            ui.HTML(energy_plot()),  # Embed energy plot as HTML
            ui.HTML(technology_plot()),  # Embed technology plot as HTML
        )

    def energy_plot():
        # Extracting year range from the slider input
        year_range = input.year_range()
        year_min, year_max = year_range[0], year_range[1]

        # Filtering data by year range
        filtered_data = data[
            (data["Year"] >= year_min) & (data["Year"] <= year_max)
        ]

        # Creating selected chart
        chart = alt.Chart(filtered_data).mark_line().encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("Primary energy consumption (TWh):Q", title="Energy (TWh)"),
            tooltip=["Year", "Primary energy consumption (TWh)"],
        ).properties(
            title="Primary Energy Consumption Over Time",
            width=600,
            height=400,
        )
        return chart.to_html()  # Convert chart to HTML

    def technology_plot():
        # Extracting year range and selected technologies from the inputs
        year_range = input.year_range()
        year_min, year_max = year_range[0], year_range[1]
        selected_technologies = input.technologies()

        # Filtering the data by year range and technologies
        filtered_data = data[
            (data["Year"] >= year_min)
            & (data["Year"] <= year_max)
            & (data["Technology"].isin(selected_technologies))
        ]

        # Creating chart
        chart = alt.Chart(filtered_data).mark_bar().encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("Electricity Generation (TWh):Q", title="Electricity Generation (TWh)"),
            color=alt.Color("Technology:N", title="Technology"),
            tooltip=["Year", "Technology", "Electricity Generation (TWh)"],
        ).properties(
            title="Electricity Generation by Technology",
            width=600,
            height=400,
        )
        return chart.to_html()  # Converting chart to HTML


# Assigning the app object
app = App(app_ui, server)
