# LEAFCLOUD: Experiment Setup & Data Gathering Protocol

This document outlines the comprehensive methodology for constructing the controlled hydroponic environment and gathering the dataset required for the LEAFCLOUD capstone project. The objective is to generate a diverse dataset of lettuce images paired with sensor data and laboratory-verified NPK values to train a Convolutional Neural Network (CNN) regression model.

## 1. Physical System Setup

The experiment requires a functional hydroponic system integrated with electronic data collection hardware.

### 1.1 Hydroponic Growing Unit
*   **System Type:** Standard hydroponic setup (Nutrient Film Technique (NFT) or Deep Water Culture (DWC)) suitable for lettuce.
*   **Components:** Grow beds/channels, reservoir, and water pumps for nutrient circulation.
*   **Crop:** Lettuce varieties common to the Davao Region.
*   **Requirement:** The system must be capable of hosting isolated batches to test varying nutrient concentrations (deficiencies, optimal ranges, and toxicities).

### 1.2 IoT Hardware (Data Acquisition)
This hardware captures "ground truth" environmental data and images.
*   **Microcontroller:** Raspberry Pi or ESP32 as the central processing unit.
*   **Visual Sensor:** High-resolution camera module for capturing leaf images.
*   **Environmental Sensors:**
    *   **pH Sensor:** Measures acidity/alkalinity.
    *   **EC Sensor (Electrical Conductivity):** Measures total nutrient strength.
    *   **Water Temperature Sensor:** Monitors solution temperature.
    *   **Ambient Sensor (DHT22):** Measures air temperature and humidity.

---

## 2. Experimental Methodology: Nutrient Variations

To train the CNN model to estimate specific NPK levels, the dataset must cover a wide spectrum of nutrient conditions. The experiment will utilize **7 distinct setups** (buckets/reservoirs) to create these conditions using individual nutrient salts.

### 2.1 The "Shopping List" (Nutrient Salts)
Commercial pre-mixed fertilizers cannot be used. The following individual salts are required to isolate N, P, and K:
*   **Calcium Nitrate:** Primary source of Nitrogen (N) and Calcium.
*   **Monopotassium Phosphate (MKP, 0-52-34):** Primary source of Phosphorus (P) and Potassium (K).
*   **Potassium Sulfate (SOP, 0-0-50):** Isolated source of Potassium (K).
*   **Magnesium Sulfate (Epsom Salt):** Source of Magnesium and Sulfur (kept constant).
*   **Micronutrient Mix:** Trace elements (Iron, Boron, etc.) (kept constant).

### 2.2 The 7 Experimental Conditions (Recipes)
*Note: "Standard Dose" refers to the manufacturer's recommended concentration for lettuce.*

1.  **Balanced (Control):**
    *   **Goal:** Optimal health.
    *   **Recipe:** Standard doses of Calcium Nitrate, MKP, Potassium Sulfate, Epsom Salt, and Micros.

2.  **Low Nitrogen (Balanced P, K):**
    *   **Goal:** Nitrogen deficiency.
    *   **Recipe:** 10-20% standard dose of Calcium Nitrate; standard MKP and Potassium Sulfate.

3.  **High Nitrogen (Balanced P, K):**
    *   **Goal:** Nitrogen toxicity.
    *   **Recipe:** 2x standard dose of Calcium Nitrate; standard MKP and Potassium Sulfate.

4.  **Low Potassium (Balanced N, P):**
    *   **Goal:** Potassium deficiency.
    *   **Recipe:** Remove Potassium Sulfate; reduce MKP by 50%; standard Calcium Nitrate.

5.  **High Potassium (Balanced N, P):**
    *   **Goal:** Potassium toxicity.
    *   **Recipe:** 2x-3x dose of Potassium Sulfate; standard Calcium Nitrate and MKP.

6.  **Low Phosphorus (Balanced N, K):**
    *   **Goal:** Phosphorus deficiency.
    *   **Recipe:** Remove MKP completely; add extra Potassium Sulfate to compensate for K loss; standard Calcium Nitrate.

7.  **High Phosphorus (Balanced N, K):**
    *   **Goal:** Phosphorus toxicity.
    *   **Recipe:** 2x dose of MKP; reduce Potassium Sulfate to balance K; standard Calcium Nitrate.

---

## 3. Data Collection Protocol

### 3.1 Data Triangulation
For every data point, three distinct types of information must be captured and linked:
1.  **Visual Data:** High-resolution image of the lettuce.
2.  **Sensor Data:** Real-time logging of pH, EC, and Temperature.
3.  **Ground Truth (Lab Data):** The exact NPK values derived from laboratory analysis.

### 3.2 Sampling Frequency
To capture the progression of nutrient stress (regression data), samples should be taken at three stages for each bucket (Total: 21 Lab Samples).
1.  **Early Stage (Days 3-5):** Visuals show faint/no signs. (Teaches "mild" levels).
2.  **Mid Stage (Days 7-10):** Visuals show clear symptoms. (Teaches "standard" deficiency patterns).
3.  **Late Stage (Days 14+):** Visuals show severe symptoms. (Teaches "critical" levels).

*Note: If budget is constrained, a minimum of 2 samples (Start/End) per bucket is viable, using mathematical interpolation for intermediate days.*

### 3.3 Laboratory Analysis
*   **Partner Facilities:** Natural Science Central Laboratory at Davao del Norte State College (DNSC) or University of the Immaculate Conception (UIC).
*   **Procedure:** Collect water samples from the specific bucket *at the same time* images and sensor readings are taken. Send to the lab for NPK analysis.
*   **Volume:** Ensure 300ml - 500ml per sample (confirm specific requirements with the lab).

---

## 4. Maintenance & Reservoir Management

### 4.1 Reservoir Volume
*   **Issue:** Sampling removes water (approx. 1.5L total for 3 samples), and plants consume water (2-4L).
*   **Restriction:** Do **not** refill with water or nutrient solution during the test phase, as this alters the concentration and ruins the "deficiency" progression.
*   **Solution:** Use large reservoirs (min. 20 Liters). This ensures the pump remains submerged even after 5-6 Liters of water loss over the 2-week period.

### 4.2 Routine Monitoring
While lab tests provide the specific NPK "labels," local sensors must continuously monitor the general state:
*   Log EC and pH daily to track general trends.
*   Correlate these simple trends with the specific lab results to refine the model's understanding.

[Next](/docs/leafcloud_experiment_setup_1.md)