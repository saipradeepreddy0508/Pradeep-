import math
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Pipe Flow Calculator", page_icon="🚰", layout="centered"
)

# Constant
G = 9.81  # Acceleration due to gravity (m/s^2)


def calculate_reynolds_number(density, velocity, diameter, viscosity):
  """Calculates Reynolds Number (Re)"""
  return (density * velocity * diameter) / viscosity


def calculate_friction_factor(reynolds, roughness, diameter):
  """Calculates Darcy Friction Factor (f)"""
  if reynolds <= 2000:
    # Laminar flow
    return 64.0 / reynolds
  else:
    # Turbulent flow (Swamee-Jain equation)
    relative_roughness = roughness / diameter
    term = (relative_roughness / 3.7) + (5.74 / (reynolds**0.9))
    f = 0.25 / (math.log10(term) ** 2)
    return f


def calculate_head_loss(f, length, diameter, velocity):
  """Calculates Head Loss (hf) in meters"""
  return f * (length / diameter) * ((velocity**2) / (2 * G))


def calculate_pressure_drop(head_loss, density):
  """Calculates Pressure Drop (delta_p) in Pascals"""
  return density * G * head_loss


def main():
  st.title("🚰 Pipe Flow Calculator")
  st.markdown(
      "Perform fluid mechanics calculations for pipe flow, including Reynolds"
      " number, Darcy friction factor, head loss, and pressure drop."
  )

  # Sidebar Navigation
  st.sidebar.title("Navigation")
  choice = st.sidebar.selectbox(
      "Select Calculation",
      [
          "1. Calculate Reynolds Number",
          "2. Calculate Darcy Friction Factor",
          "3. Calculate Head Loss",
          "4. Calculate Pressure Drop",
      ],
  )

  st.markdown("---")

  if choice == "1. Calculate Reynolds Number":
    st.header("Reynolds Number ($Re$)")
    st.markdown(
        "Predicts whether fluid flow is laminar, transitional, or turbulent."
    )

    col1, col2 = st.columns(2)
    with col1:
      rho = st.number_input(
          "Fluid Density ($\rho$ in kg/m³)", value=998.2, format="%.2f"
      )
      v = st.number_input("Fluid Velocity ($v$ in m/s)", value=1.5, format="%.2f")
    with col2:
      d = st.number_input(
          "Pipe Inner Diameter ($d$ in m)", value=0.05, format="%.4f"
      )
      mu = st.number_input(
          "Dynamic Viscosity ($\mu$ in Pa·s)", value=0.001002, format="%.6f"
      )

    if st.button("Calculate Reynolds Number", type="primary"):
      re = calculate_reynolds_number(rho, v, d, mu)
      st.success(f"**Result: Reynolds Number (Re) = {re:,.2f}**")

      if re < 2000:
        st.info("Flow Regime: **Laminar**")
      elif re <= 4000:
        st.warning("Flow Regime: **Transitional**")
      else:
        st.error("Flow Regime: **Turbulent**")

  elif choice == "2. Calculate Darcy Friction Factor":
    st.header("Darcy Friction Factor ($f$)")
    st.markdown(
        "Calculates friction factor based on flow regime using the Swamee-Jain"
        " equation for turbulent flow."
    )

    col1, col2 = st.columns(2)
    with col1:
      re = st.number_input(
          "Reynolds Number ($Re$)", value=25000.0, format="%.2f"
      )
      d = st.number_input(
          "Pipe Inner Diameter ($d$ in m)", value=0.05, format="%.4f"
      )
    with col2:
      epsilon = st.number_input(
          "Pipe Roughness ($\epsilon$ in m)",
          value=0.000045,
          format="%.6f",
          help="e.g., 0.000045 for commercial steel",
      )

    if st.button("Calculate Friction Factor", type="primary"):
      f = calculate_friction_factor(re, epsilon, d)
      st.success(f"**Result: Darcy Friction Factor ($f$) = {f:.5f}**")

  elif choice == "3. Calculate Head Loss":
    st.header("Head Loss ($h_f$)")
    st.markdown(
        "Calculates frictional head loss along a straight pipe section."
    )

    col1, col2 = st.columns(2)
    with col1:
      f = st.number_input(
          "Darcy Friction Factor ($f$)", value=0.022, format="%.5f"
      )
      L = st.number_input("Pipe Length ($L$ in m)", value=100.0, format="%.2f")
    with col2:
      d = st.number_input(
          "Pipe Inner Diameter ($d$ in m)", value=0.05, format="%.4f"
      )
      v = st.number_input("Fluid Velocity ($v$ in m/s)", value=1.5, format="%.2f")

    if st.button("Calculate Head Loss", type="primary"):
      hf = calculate_head_loss(f, L, d, v)
      st.success(f"**Result: Head Loss ($h_f$) = {hf:.4f} m**")

  elif choice == "4. Calculate Pressure Drop":
    st.header("Pressure Drop ($\Delta P$)")
    st.markdown(
        "Calculates the pressure drop resulting from frictional head loss."
    )

    col1, col2 = st.columns(2)
    with col1:
      hf = st.number_input("Head Loss ($h_f$ in m)", value=3.5, format="%.4f")
    with col2:
      rho = st.number_input(
          "Fluid Density ($\rho$ in kg/m³)", value=998.2, format="%.2f"
      )

    if st.button("Calculate Pressure Drop", type="primary"):
      dp = calculate_pressure_drop(hf, rho)
      st.success(
          f"**Result: Pressure Drop ($\Delta P$) = {dp:,.2f} Pa"
          f" ({dp/1000:,.3f} kPa)**"
      )


if __name__ == "__main__":
  main()
