---
config:
  layout: fixed
  theme: base
---
flowchart TD
 subgraph Frontend["Frontend"]
        A1["index.html"]
        A2["JavaScript"]
        A3["CSS Styles"]
  end
 subgraph subGraph1["Backend (Flask)"]
        B1["app.py"]
        B2["Routes"]
        B3["Form Processing"]
        B4["Data Validation"]
  end
 subgraph subGraph2["AI Components"]
        D1["Classification of Diabetes Types"]
        D2["Lifestyle-Based Risk Assessment"]
        D3["Projection of Diabetic Cases"]
        D4["Prediction of Gestational Diabetes"]
        E1["FAQ Dataset"]
        E2["TF-IDF Vectorizer"]
  end
    A["Client Browser"] -- HTTP Requests --> B["Flask Web Server"]
    B -- HTTP Responses --> A
    B -- Query/Update --> C["SQLite Database"]
    B -- Predictions ------> D["ML Models"]
    B -- Chat Requests --> E["Chatbot"]
    B -- Server --> F["Static Files"]
    A --> A1
    A1 --> A2 & A3
    B --> B1
    B1 --> B2
    B2 --> B3 & B4
    D --> D1 & D2 & D3 & D4
    E --> E1 & E2
    B3 -- Process Form Data --> D
    B4 -- Validate Input --> C
    E -- Generate Responses --> B
    D2 <--> F1["Decision Tree Classifier"]
    D1 <--> F2["Random Forest Classifier"]
    D4 <--> F3["Decision Tree Classifier"]
    D3 <--> F4["Linear Regression"]
    F1 <--> G1["Dataset"]
    F2 <--> G2["Dataset"]
    F3 <--> G3["Dataset"]
    F4 <--> G4["Dataset"]
    G1 ---> K["Database"]
    G2 ---> K
    G3 ---> K
    G4 ---> K
