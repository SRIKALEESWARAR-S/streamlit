import streamlit as st
import numpy as np

def angular_frequency(theta, time):
    """
    Compute angular frequency ω = θ / t
    """

    # Scalar case
    if isinstance(theta, (int, float)) and isinstance(time, (int, float)):
        if theta < 0 or theta > 360:
            raise ValueError("Theta must be between 0 and 360 degrees")
        if time <= 0:
            raise ValueError("Time must be positive")

        theta_rad = np.deg2rad(theta)
        return theta_rad / time

    # Iterable case
    theta_arr = np.array(theta, dtype=float)
    time_arr = np.array(time, dtype=float)

    if theta_arr.shape != time_arr.shape:
        raise ValueError("Theta and time must have same length")

    if np.any(theta_arr < 0) or np.any(theta_arr > 360):
        raise ValueError("Theta must be between 0 and 360 degrees")

    if np.any(time_arr <= 0):
        raise ValueError("Time must be positive")

    theta_rad = np.deg2rad(theta_arr)
    return theta_rad / time_arr


# ---------------- STREAMLIT UI ---------------- #

st.set_page_config(page_title="Angular Frequency Calculator", layout="centered")

st.title("Angular Frequency Calculator")
st.write("Formula:  ω = θ / t  (θ in radians)")

mode = st.radio(
    "Choose input type",
    ("Single value", "Multiple values")
)

try:
    if mode == "Single value":
        theta = st.number_input("Theta (degrees)", min_value=0.0, max_value=360.0)
        time = st.number_input("Time (seconds)", min_value=0.0001)

        if st.button("Calculate"):
            omega = angular_frequency(theta, time)
            st.success(f"Angular Frequency ω = {omega:.4f} rad/s")

    else:
        st.write("Enter values separated by commas")

        theta_text = st.text_input("Theta values (degrees)", "90, 180, 270")
        time_text = st.text_input("Time values (seconds)", "1, 2, 3")

        if st.button("Calculate"):
            theta_list = [float(x) for x in theta_text.split(",")]
            time_list = [float(x) for x in time_text.split(",")]

            omega = angular_frequency(theta_list, time_list)

            st.success("Angular Frequency (rad/s)")
            st.write(omega)

            st.line_chart(omega)

except Exception as e:
    st.error(str(e))

