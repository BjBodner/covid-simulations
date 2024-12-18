# Epidemic Simulator

![Alt text](./media/demo.gif)

A real-time visualization tool for simulating epidemic spread using Streamlit and Plotly. This interactive simulation allows users to adjust various parameters and observe how diseases spread through a population.

## Installation & How to Run

### Method 1: Running with Streamlit directly

1. Clone the repository:
```bash
git clone https://github.com/BjBodner/epidemic-simulator.git
cd epidemic-simulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run src/main.py
```

The application will be available at `http://localhost:8501`

### Method 2: Running with Docker

1. Clone the repository:
```bash
git clone https://github.com/BjBodner/epidemic-simulator.git
cd epidemic-simulator
```

2. Build the Docker image:
```bash
docker build -t epidemic-simulator .
```

3. Run the container:
```bash
docker run -p 8501:8501 epidemic-simulator
```

The application will be available at `http://localhost:8501`

## Usage

1. Open the application in your web browser
2. Use the sidebar sliders to adjust simulation parameters:
   - Number of People: Total population size
   - Initial Infected: Starting number of infected individuals
   - Movement Amount: How much individuals move
   - Infection Radius: Distance within which infection can spread
   - Infection Probability: Likelihood of infection within radius
   - Simulation Speed: Control the speed of the simulation
3. Click the "Start/Stop" button to control the simulation
4. Parameters can be adjusted in real-time while the simulation is running


## Contributing
Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License
MIT

## Author
Benjamin J. Bodner