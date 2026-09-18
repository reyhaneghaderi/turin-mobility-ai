import streamlit as st
from pathlib import Path
import base64

from assistant import run_agent


# --------------------------------------------------
# Background image
# --------------------------------------------------

background_path = Path(__file__).parent / "background.jpg"

with open(background_path, "rb") as image_file:
    encoded_image = base64.b64encode(
        image_file.read()
    ).decode()


# --------------------------------------------------
# Page style
# --------------------------------------------------

st.markdown(
    f"""
    <style>

    /* --------------------------------------------------
       Background
    -------------------------------------------------- */

    .stApp {{
        background-image:
            linear-gradient(
                rgba(255, 255, 255, 0.68),
                rgba(255, 255, 255, 0.68)
            ),
            url("data:image/jpg;base64,{encoded_image}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;

        /* Space so footer does not cover content */
        padding-bottom: 70px;
    }}


    /* --------------------------------------------------
       Main title
    -------------------------------------------------- */

    h1 {{
        font-size: 52px !important;
        font-weight: 800 !important;
        color: #111111 !important;
    }}


    /* --------------------------------------------------
       Normal text
    -------------------------------------------------- */

    .stMarkdown p {{
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #111111 !important;
        line-height: 1.6 !important;
    }}


    /* --------------------------------------------------
       Question label
    -------------------------------------------------- */

    .stTextInput label p {{
        font-size: 19px !important;
        font-weight: 700 !important;
        color: #111111 !important;
    }}


    /* --------------------------------------------------
       Question box
    -------------------------------------------------- */

    div[data-baseweb="input"] {{
        border: 3px solid #222222 !important;
        border-radius: 10px !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
    }}


    /* Question box when clicked */
    div[data-baseweb="input"]:focus-within {{
        border: 3px solid #000000 !important;
        box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.15) !important;
    }}


    /* Text inside question box */
    .stTextInput input {{
        font-size: 19px !important;
        color: #111111 !important;
        padding: 12px !important;
    }}


    /* Placeholder text */
    .stTextInput input::placeholder {{
        color: #666666 !important;
        opacity: 1 !important;
    }}


    /* --------------------------------------------------
       Answer title
    -------------------------------------------------- */

    h2, h3 {{
        color: #111111 !important;
        font-weight: 750 !important;
    }}


    /* --------------------------------------------------
       Fixed demo limitation footer
    -------------------------------------------------- */

    .fixed-demo-note {{
        position: fixed;

        bottom: 0;
        left: 0;

        width: 100%;

        background-color: rgba(255, 255, 255, 0.95);

        border-top: 1px solid #cccccc;

        padding: 7px 15px;

        text-align: center;

        font-size: 11px !important;
        font-weight: 400 !important;

        color: #555555 !important;

        line-height: 1.4;

        z-index: 9999;

        box-sizing: border-box;
    }}


    .fixed-demo-note b {{
        font-weight: 700 !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Page content
# --------------------------------------------------

st.title("Turin Mobility AI Assistant")

st.write(
    """
Fai domande sul traffico, parcheggi, ZTL e limitazioni alla mobilità di Torino.

Ask questions about Turin traffic, parking, ZTL rules and mobility restrictions.
"""
)


# --------------------------------------------------
# Question box
# --------------------------------------------------

question = st.text_input(
    "Ask a question in English or Italian / Fai una domanda in inglese o italiano:",
    placeholder="Type your question here / Scrivi qui la tua domanda..."
)


# --------------------------------------------------
# Example questions
# --------------------------------------------------

st.subheader("💡 Example questions / Esempi di domande")

left_col, right_col = st.columns(2)


with left_col:

    st.info(
        """
🚗 **Parking / Parcheggi**

• Quale parcheggio ha più posti liberi?  
• Which parking has the most free spaces?


🚦 **Traffic / Traffico**

• Qual è la velocità media del traffico?  
• What is the average traffic speed?
"""
    )


with right_col:

    st.info(
        """
📄 **Rules & ZTL / Regole e ZTL**

• Quanto costa la sosta nella ZTL?  
• How much does parking cost in the ZTL?


🔄 **Combined / Domande combinate**

• Quanto costa la sosta nella ZTL e qual è la velocità media del traffico?  
• How much does parking cost in the ZTL and what is the average traffic speed?
"""
    )


# --------------------------------------------------
# Fixed demo limitation note
# --------------------------------------------------
# IMPORTANT:
# This is BEFORE "if question",
# so it is displayed even if run_agent() later fails.
# --------------------------------------------------

st.markdown(
    """
    <div class="fixed-demo-note">

        ⚠️ <b>Demo note / Nota sulla demo:</b>

        This prototype uses a free-tier LLM API with limited daily requests.
        If the limit is reached, AI responses may be temporarily unavailable.

        &nbsp; | &nbsp;

        Questo prototipo utilizza un'API LLM gratuita con un limite giornaliero
        di richieste. Se il limite viene raggiunto, le risposte AI potrebbero
        essere temporaneamente non disponibili.

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# AI answer
# --------------------------------------------------

if question:

    try:

        with st.spinner("Thinking / Elaborazione..."):

            answer = run_agent(question)


        st.subheader("Answer / Risposta")


        # --------------------------------------------------
        # One simple database value
        # --------------------------------------------------

        if (
            isinstance(answer, list)
            and len(answer) == 1
            and isinstance(answer[0], dict)
            and len(answer[0]) == 1
        ):

            key, value = next(
                iter(answer[0].items())
            )

            label = (
                key.replace("_", " ")
                .title()
            )


            if isinstance(
                value,
                (int, float)
            ):

                st.metric(
                    label,
                    f"{value:.2f}"
                )

            else:

                st.write(value)


        # --------------------------------------------------
        # Multiple database rows
        # --------------------------------------------------

        elif (
            isinstance(answer, list)
            and len(answer) > 0
            and isinstance(answer[0], dict)
        ):

            st.dataframe(
                answer,
                use_container_width=True,
                hide_index=True
            )


        # --------------------------------------------------
        # Empty database result
        # --------------------------------------------------

        elif (
            isinstance(answer, list)
            and len(answer) == 0
        ):

            st.info(
                """
No data was found for this question.

Nessun dato trovato per questa domanda.
"""
            )


        # --------------------------------------------------
        # RAG / BOTH / normal text answer
        # --------------------------------------------------

        else:

            st.write(answer)


    # --------------------------------------------------
    # Friendly error message
    # --------------------------------------------------

    except Exception as e:

        st.subheader("Answer / Risposta")

        st.error(
            """
The service is temporarily unavailable.

This can happen because of the free API usage limit
or a temporary database connection problem.

Please try again later.

---

Il servizio è temporaneamente non disponibile.

Questo può accadere a causa del limite dell'API gratuita
o di un problema temporaneo di connessione al database.

Riprova più tardi.
"""
        )

        # The real technical error is printed in Streamlit logs
        # instead of showing the traceback to the public user.
        print(
            f"Turin Mobility AI error: {type(e).__name__}: {e}"
        )