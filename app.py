import math
import streamlit as st

st.set_page_config(page_title="Unintuitive Probability", page_icon="🎲", layout="centered")

def collision_probability(group_size: int, choices: int) -> float:
    """Probability that at least two people choose the same option."""
    if group_size <= 1:
        return 0.0
    if group_size > choices:
        return 1.0

    # Probability everyone chooses a different option:
    # (choices / choices) * ((choices-1) / choices) * ...
    probability_all_different = 1.0
    for person in range(group_size):
        probability_all_different *= (choices - person) / choices

    return 1.0 - probability_all_different


def minimum_group_for_probability(choices: int, target: float = 0.5) -> int:
    """Smallest group size whose collision probability reaches the target."""
    for group_size in range(1, choices + 1):
        if collision_probability(group_size, choices) >= target:
            return group_size
    return choices


st.title("Unintuitive Probability")
st.write(
    "Explore how likely it is that at least two people in a group share "
    "the same randomly selected option."
)

example = st.radio(
    "Choose an example",
    ["Shared number", "Shared birth month"],
    horizontal=True,
)

if example == "Shared number":
    st.subheader("Shared number")
    st.write(
        "If 10 people each randomly pick a whole number from 1 to 100, "
        "what is the probability that at least two people pick the same number?"
    )

    group_size = st.slider("Number of people", min_value=1, max_value=100, value=10)
    choices = 100
    choice_label = "100 possible numbers"

    st.metric(
        "Probability of at least one shared number",
        f"{collision_probability(group_size, choices):.2%}",
    )

    st.markdown("**Why?**")
    st.write(
        "It is easier to first calculate the probability that everyone picks "
        "a different number, then subtract that result from 1."
    )
    st.latex(
        r"P(\text{at least one match})"
        r"=1-P(\text{all different})"
    )
    st.latex(
        r"=1-\\left(\\frac{100}{100}\\right)"
        r"\\left(\\frac{99}{100}\\right)"
        r"\\cdots"
        r"\\left(\\frac{100-n+1}{100}\\right)"
    )
    st.caption(
        f"Here, n = {group_size}. There are {choice_label}. "
        "Each person independently chooses one number, with every number equally likely."
    )

else:
    st.subheader("Shared birth month")
    st.write(
        "Assuming all 12 months are equally likely, how many people are needed "
        "for the probability that at least two share a birth month to reach 50%?"
    )

    group_size = st.slider("Number of people", min_value=1, max_value=12, value=5)
    choices = 12
    probability = collision_probability(group_size, choices)
    threshold_group = minimum_group_for_probability(choices, 0.5)

    st.metric(
        "Probability of at least two sharing a birth month",
        f"{probability:.2%}",
    )

    if probability >= 0.5:
        st.success(f"At {group_size} people, the probability is at least 50%.")
    else:
        st.info(f"At {group_size} people, the probability is still below 50%.")

    st.markdown("**Why is the answer 5 people?**")
    st.write(
        "Calculate the chance that everyone has a different birth month. "
        "For each additional person, there are fewer months left that would "
        "avoid a match. Subtract that probability from 1."
    )
    st.latex(
        r"P(\text{at least one match})"
        r"=1-\\left(\\frac{12}{12}\\right)"
        r"\\left(\\frac{11}{12}\\right)"
        r"\\cdots"
        r"\\left(\\frac{12-n+1}{12}\\right)"
    )
    st.write(
        f"- 4 people: **{collision_probability(4, 12):.2%}** chance of a match.\n"
        f"- 5 people: **{collision_probability(5, 12):.2%}** chance of a match."
    )
    st.caption(
        f"Therefore, the smallest group size reaching 50% is **{threshold_group}**. "
        "This simplified model assumes each month is equally likely and ignores "
        "real-world differences in birth rates."
    )

st.divider()
st.caption(
    "Key idea: a match can occur between any pair of people—not just when "
    "someone matches a particular person's choice."
)
