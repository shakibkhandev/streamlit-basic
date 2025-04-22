import streamlit as st
from datetime import datetime

# Sidebar
with st.sidebar:
    st.markdown("## Settings ⚙️")
    # Sidebar text input
    user_name = st.text_input("Enter your name", "Guest")
    # Sidebar date input
    user_date = st.date_input("Select a date", datetime.now())
    st.write(f"Selected date: {user_date}")

st.title("Hello world!")
st.markdown("## Welcome to our *interactive* app! ✨")
st.text("Welcome to our app")

# Create three columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Column 1")
    # Button with success message
    if st.button("Click me!"):
        st.success("You clicked the button!")
    
    # Checkbox
    show_text = st.checkbox("Show additional text")
    if show_text:
        st.write("You checked the box!")

with col2:
    st.markdown("### Column 2")
    # Radio buttons
    favorite_color = st.radio(
        "What's your favorite color?",
        ["Red", "Green", "Blue"]
    )
    st.write(f"Your favorite color is {favorite_color}")

    # Selectbox
    option = st.selectbox(
        'How would you like to be contacted?',
        ['Email', 'Phone', 'WhatsApp']
    )
    st.write(f'You selected: {option}')

with col3:
    st.markdown("### Column 3")
    # Slider
    age = st.slider('How old are you?', 0, 100, 25)
    st.write(f"I'm {age} years old")

    # Number input
    number = st.number_input('Insert a number', min_value=0, max_value=100, value=50)
    st.write('The current number is ', number)

# Text input in main area
user_story = st.text_area("Tell us your story", "Type here...")
if user_story != "Type here...":
    st.write("Your story:", user_story)

# Expander
with st.expander("Click to see more details"):
    st.markdown("""
    ### Additional Information
    This is hidden content that can be expanded!
    - Point 1
    - Point 2
    - Point 3
    """)

# Display sample image
st.markdown("### Sample Image")
st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", 
         caption="Streamlit Logo",
         width=200)

# Advanced markdown
st.markdown("""
---
## Formatted Text Examples
- **Bold text**
- *Italic text*
- `Code format`
- [Streamlit Documentation](https://docs.streamlit.io)

> This is a blockquote

```python
# This is a code block
def hello():
    print("Hello, World!")
```
---
""")