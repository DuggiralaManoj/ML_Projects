const apiUrl = "http://127.0.0.1:5000/predict";

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('diseaseForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const disease = form.getAttribute('data-disease');
        const inputs = form.querySelectorAll('input[name="feature"]');
        const features = Array.from(inputs).map(input => parseFloat(input.value));

        // Store input values for the report
        const inputData = {
            disease: disease,
            features: features,
            labels: getLabelsForDisease(disease)
        };

        fetch(`${apiUrl}/${disease}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ features: features })
        })
        .then(res => res.json())
        .then(data => {
            if (data.prediction !== undefined) {
                // Store input data in sessionStorage for the report
                sessionStorage.setItem('inputData', JSON.stringify(inputData));
                sessionStorage.setItem('prediction', data.prediction);

                // Redirect to result page
                window.location.href = `result.html?result=${data.prediction}&disease=${disease}`;
            } else {
                alert('Prediction failed. Try again.');
            }
        })
        .catch(() => alert('Server error. Ensure API is running.'));
    });
});

function getLabelsForDisease(disease) {
    const labels = {
        'diabetes': [
            'Pregnancies',
            'Glucose Level (mg/dL)',
            'Blood Pressure (mm Hg)',
            'Skin Thickness (mm)',
            'Insulin (mu U/ml)',
            'BMI',
            'Diabetes Pedigree Function',
            'Age (years)'
        ],
        'heart_disease': [
            'Age (years)',
            'Sex (0=female, 1=male)',
            'Chest Pain Type (0-3)',
            'Resting Blood Pressure (mm Hg)',
            'Cholesterol Level (mg/dl)',
            'Fasting Blood Sugar >120 mg/dl (1=true, 0=false)',
            'Resting ECG (0-2)',
            'Max Heart Rate Achieved',
            'Exercise Induced Angina (1=yes, 0=no)',
            'ST Depression Induced by Exercise',
            'Peak Exercise ST Segment (1=upsloping, 2=flat, 3=downsloping)',
            'Number of Major Vessels (0-3)',
            'Thalassemia (1=normal, 2=fixed defect, 3=reversible defect)'
        ],
        'breast_cancer': [
            'Mean Radius', 'Mean Texture', 'Mean Perimeter', 'Mean Area', 'Mean Smoothness',
            'Mean Compactness', 'Mean Concavity', 'Mean Concave Points', 'Mean Symmetry', 'Mean Fractal Dimension',
            'SE Radius', 'SE Texture', 'SE Perimeter', 'SE Area', 'SE Smoothness',
            'SE Compactness', 'SE Concavity', 'SE Concave Points', 'SE Symmetry', 'SE Fractal Dimension',
            'Worst Radius', 'Worst Texture', 'Worst Perimeter', 'Worst Area', 'Worst Smoothness',
            'Worst Compactness', 'Worst Concavity', 'Worst Concave Points', 'Worst Symmetry', 'Worst Fractal Dimension'
        ]
    };
    return labels[disease] || [];
}