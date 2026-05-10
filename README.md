# 🌪️ HK Tropical Cyclone Impact – Scrollytelling

An interactive data story exploring 35 years of tropical cyclone impacts on Hong Kong, based on 207 records from the Hong Kong Observatory (1988–2023). Navigate through chapters, filter by signal strength and time, and explore where storms hit, how they affect different stations, and what their economic and human cost has been.

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white)
![ECharts](https://img.shields.io/badge/ECharts-AA344D?style=flat-square&logo=apache-echarts&logoColor=white)

## ✨ Features

- **Scrollytelling narrative** – 13 chapters explaining cyclone science, warning signals, and local impacts.
- **Interactive timeline + signal filter** – Use the slider to choose any year range (1988–2023) and checkboxes to select which cyclone warning signals to show.
- **Multi‑view map** (Leaflet)
  - **Cyclone view** – Closest approaches coloured by signal, with size reflecting economic loss.
  - **Wind view** – Average maximum gust across Hong Kong’s weather stations.
  - **Rainfall view** – Average rainfall recorded at each station.
- **Dynamic statistics cards** – Total passages, loss, peak surge, deaths, and maximum gust update with every filter change.
- **ECharts visualisations**
  - Stacked bar chart of cyclone frequency by year and signal.
  - Radar chart comparing average impact dimensions (gust, rain, surge, loss, people affected) per signal level.
  - Bubble chart of economic loss over time (log scale), bubble size proportional to people affected.
  - Box plot of economic loss distribution by signal.
  - Casualty & affected population chart over time.
- **Responsive design** – Optimised for desktop and mobile screens.
- **Smooth section reveal** – Fade‑in animations as you scroll.

## 🧑‍💻 Tech Stack

| Tool | Purpose |
|------|---------|
| [Leaflet](https://leafletjs.com/) | Interactive map with custom markers and distance rings |
| [ECharts](https://echarts.apache.org/) | All statistical charts (bar, radar, scatter, box plot, line) |
| [noUiSlider](https://refreshless.com/nouislider/) | Dual‑handle timeline slider for year selection |
| [Font Awesome](https://fontawesome.com/) | Icons across the UI |
| Vanilla HTML/CSS/JS | Layout, styling, data wrangling, and interactivity |

All data is embedded directly in the HTML file; no external API calls are required.

## 📊 Data

- **Source**: Hong Kong Observatory Tropical Cyclone Impact Dataset (1988–2023)
- **207 cyclone records** with the following attributes:
  `year, name, signal, distance, bearing, surge, dead, missing, injured, affected, loss (HK$ million), maxGust (km/h), maxRain (mm)`
- Additional data: wind (gust/mean) and rainfall measurements from dozens of Hong Kong weather stations, linked to each cyclone event.

> ℹ️ Losses are reported in nominal Hong Kong dollars (millions).

## 🚀 How to Run

1. Download or clone this repository.
2. Open `Interactive map.html` in any modern browser (Chrome, Firefox, Edge, Safari).
3. That’s it – everything works locally, no build step or server needed.

