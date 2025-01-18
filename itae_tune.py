import streamlit as st
import math

# Function to calculate PI or PID settings based on FOPTD parameters and selected type
def calculate_controller_settings(type_of_input, type_of_controller, K, theta, tau):
    # Table values
    table = {
        ("Disturbance", "PI"): {"P": (0.859, -0.977), "I": (0.674, -0.680)},
        ("Disturbance", "PID"): {"P": (1.357, -0.947), "I": (0.842, -0.738), "D": (0.381, 0.995)},
        ("Set point", "PI"): {"P": (0.586, -0.916), "I": (1.03, -0.165)},
        ("Set point", "PID"): {"P": (0.965, -0.850), "I": (0.796, -0.1465), "D": (0.308, 0.929)},
    }

    settings = {}

    if type_of_input in ["Disturbance", "Set point"] and type_of_controller in ["PI", "PID"]:
        modes = table[(type_of_input, type_of_controller)]
        for mode, (A, B) in modes.items():
            if mode == "P":
                settings["Kc"] = (A * (theta / tau) ** B) / K
            elif mode == "I":
                if type_of_input == "Set point":
                    settings["tau_I"] = tau / (A + B * (theta / tau))
                else:
                    settings["tau_I"] = tau / (A * (theta / tau) ** B)
            elif mode == "D":
                settings["tau_D"] = A * (theta / tau) ** B

    return settings

# Streamlit interface
st.title("FOPTD Model Controller Settings Calculator")

# Inputs
st.header("Input Parameters")

K = st.number_input("Enter K (Process Gain):", min_value=0.0, format="%.5f")
theta = st.number_input("Enter \u03b8 (theta):", min_value=0.0, format="%.5f")
tau = st.number_input("Enter \u03c4 (tau):", min_value=0.0, format="%.5f")

type_of_input = st.selectbox("Select Type of Input:", ["Disturbance", "Set point"])
type_of_controller = st.selectbox("Select Type of Controller:", ["PI", "PID"])

# Calculate button
if st.button("Calculate Settings"):
    if K > 0 and theta > 0 and tau > 0:
        settings = calculate_controller_settings(type_of_input, type_of_controller, K, theta, tau)

        if settings:
            st.header("Controller Settings")
            st.success("Calculation Successful!")
            st.markdown("<div style='background-color: #f0f8ff; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
            for key, value in settings.items():
                st.markdown(f"<p style='font-size: 18px;'><strong>{key}:</strong> {value:.5f}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("Invalid input combination. Please check your selections.")
    else:
        st.error("Please enter positive values for K, \u03b8, and \u03c4.")
