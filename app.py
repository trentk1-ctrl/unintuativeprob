
import streamlit as st
import math

st.set_page_config(
    page_title="Unintuitive Probability",
    page_icon="🎲",
    layout="centered"
)

def collision_probability(n, choices):
    """Probability that at least two people select the same option."""
    if n <= 1:
        return 0.0
    if n > choices:
        return 1.0

    log_distinct = sum(
        math.log1p(-i / choices) for i in range(n)
    )
    return -math.expm1(log_distinct)


def minimum_group(choices, target=0.5):
    for n in range(1, choices + 1):
        if collision_probability(n, choices) >= target:
            return n
    return choices


st.title("Unintuitive Probability")

st.write(
    "Two examples demonstrating how probability can be "
    "surprisingly unintuitive."
)

example = st.radio(
    "Choose an example:",
    ["Shared Number", "Shared Birth Month"],
    horizontal=True
)

# Separate reveal states for each example
if "number_revealed" not in st.session_state:
    st.session_state.number_revealed = False

if "month_revealed" not in st.session_state:
    st.session_state.month_revealed = False


# ==========================================
# SHARED NUMBER
# ==========================================

if example == "Shared Number":

    st.divider()

    st.markdown("## How likely is it that two people pick the same number?")

    st.markdown(
        """
        Imagine 10 people are each asked to randomly pick
        a whole number between **1 and 100**.

        **What is the probability that at least two people
        pick the same number?**
        """
    )

    st.info("Think about your answer before revealing the probability.")

    if not st.session_state.number_revealed:

        if st.button("Reveal Probability", type="primary"):
            st.session_state.number_revealed = True
            st.rerun()

    else:

        st.success("The probability is 37.184%!")

        st.markdown("### Now experiment with the group size")

        n = st.slider(
            "Number of people",
            min_value=1,
            max_value=101,
            value=10,
            key="number_slider"
        )

        probability = collision_probability(n, 100)

        st.metric(
            "Probability of at least one match",
            f"{probability:.8%}"
        )

        if n > 100:
            st.success("A match is guaranteed!")
        else:
            st.write(
                f"With {n} people and 100 possible numbers, "
                f"the probability of a match is {probability:.8%}."
            )

        with st.expander("Why is the probability so high? (Reasoning and formula)"):

            st.write(
                "Instead of calculating the probability that two "
                "people match, it is easier to calculate the probability "
                "that EVERY person picks a different number."
            )

            st.latex(
                r"P(\text{match})=1-P(\text{all different})"
            )

            st.latex(
                r"=1-\prod_{i=0}^{n-1}\frac{100-i}{100}"
            )

            st.write(
                "The first person can pick any number. "
                "The second has 99 numbers remaining that avoid a match. "
                "The third has 98, and so on."
            )

            st.write(
                "Subtracting the probability that everyone picks "
                "a different number from 1 gives the probability "
                "of at least one shared number."
            )


# ==========================================
# SHARED BIRTH MONTH
# ==========================================

else:

    st.divider()

    st.markdown("## How many people does it take to share a birth month?")

    st.markdown(
        """
        Assume there are 12 months in a year, and each month
        is equally likely to be someone's birth month.

        **How many people must be in a group for the probability
        of at least two people sharing a birth month to reach 50%?**
        """
    )

    st.info("Make a prediction before revealing the answer.")

    if not st.session_state.month_revealed:

        if st.button("Reveal Answer", type="primary"):
            st.session_state.month_revealed = True
            st.rerun()

    else:

        answer = minimum_group(12)
        answer_probability = collision_probability(answer, 12)

        st.success(f"Only {answer} people are needed!")

        st.write(
            f"With {answer} people, the probability of at least "
            f"two sharing a birth month is {answer_probability:.8%}."
        )

        st.markdown("### Now experiment with the group size")

        n = st.slider(
            "Number of people",
            min_value=1,
            max_value=12,
            value=5,
            key="month_slider"
        )

        probability = collision_probability(n, 12)

        st.metric(
            "Probability of at least one shared birth month",
            f"{probability:.8%}"
        )

        if probability >= 0.5:
            st.success("The probability has reached at least 50%!")
        else:
            st.info("The probability is still below 50%.")

        with st.expander("Why is the answer 5? (Reasoning and formula)"):

            st.write(
                "We calculate the probability that everyone has "
                "a different birth month, then subtract it from 1."
            )

            st.latex(
                r"P(\text{match})=1-P(\text{all different})"
            )

            st.latex(
                r"=1-\prod_{i=0}^{n-1}\frac{12-i}{12}"
            )

            st.write(
                "For the first person, any month is possible. "
                "For the second person, 11 of the 12 months avoid "
                "a match. For the third, 10 of the 12 months avoid "
                "a match, and so on."
            )

            st.write(
                f"4 people: {collision_probability(4, 12):.5%} chance of a match."
            )

            st.write(
                f"5 people: {collision_probability(5, 12):.5%} chance of a match."
            )

            st.write(
                "The model assumes every month is equally likely "
                "and that birth months are independent."
            )


st.divider()

st.caption(
    "Probability simulation | Assumes independent, equally likely selections."
)
