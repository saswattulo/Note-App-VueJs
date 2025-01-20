<template>
  <div class="file-upload">
    <h1>Upload CSV File</h1>
    <input type="file" @change="selectFile" />
    <button :disabled="!file" @click="uploadFile">Upload</button>

    <div v-if="loading" class="loading">Uploading and analyzing file...</div>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="analytics && !loading" class="analytics-dashboard">
      <!-- Navbar -->
      <nav class="chart-navbar">
        <button
          v-for="(chart, index) in chartTitles"
          :key="index"
          :class="{ active: activeChart === chart.key }"
          @click="activeChart = chart.key"
        >
          {{ chart.title }}
        </button>
      </nav>

      <!-- Charts -->
      <div class="chart-container">
        <!-- Salary Distribution Chart -->
        <div v-if="activeChart === 'salaryDistribution'">
          <h2>Salary Distribution</h2>
          <Bar
            v-if="salaryDistributionChartData"
            :data="salaryDistributionChartData"
            :options="barChartOptions"
          />
        </div>

        <!-- Age Distribution Chart -->
        <div v-if="activeChart === 'ageDistribution'">
          <h2>Age Distribution</h2>
          <Bar
            v-if="ageDistributionChartData"
            :data="ageDistributionChartData"
            :options="barChartOptions"
          />
        </div>

        <!-- Joining Trend Chart -->
        <div v-if="activeChart === 'joiningTrend'">
          <h2>Employees Joining Trend</h2>
          <Line
            v-if="joiningTrendChartData"
            :data="joiningTrendChartData"
            :options="lineChartOptions"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { Bar, Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
} from "chart.js";

// Register required Chart.js components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
);

// Reactive state variables
import { ref, computed } from "vue";

const file = ref(null);
const analytics = ref(null);
const loading = ref(false);
const error = ref(null);
const activeChart = ref("salaryDistribution");

// Chart titles
const chartTitles = [
  { key: "salaryDistribution", title: "Salary Distribution" },
  { key: "ageDistribution", title: "Age Distribution" },
  { key: "joiningTrend", title: "Joining Trend" },
];

// Chart options
const barChartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  aspectRatio: 2,
};

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  aspectRatio: 2,
};

const salaryDistributionChartData = computed(() => {
  if (!analytics.value?.salary_distribution) return null;

  return {
    labels: analytics.value.salary_distribution.labels,
    datasets: [
      {
        label: "Employees Count",
        backgroundColor: "#4CAF50",
        data: analytics.value.salary_distribution.values,
      },
    ],
  };
});

const ageDistributionChartData = computed(() => {
  if (!analytics.value?.age_distribution) return null;

  return {
    labels: analytics.value.age_distribution.labels,
    datasets: [
      {
        label: "Employees Count",
        backgroundColor: "#FFC107",
        data: analytics.value.age_distribution.values,
      },
    ],
  };
});

const joiningTrendChartData = computed(() => {
  if (!analytics.value?.joining_trend) return null;

  return {
    labels: analytics.value.joining_trend.labels,
    datasets: [
      {
        label: "Employees Count",
        backgroundColor: "#2196F3",
        borderColor: "#2196F3",
        data: analytics.value.joining_trend.values,
        fill: false,
      },
    ],
  };
});

// Methods
const selectFile = (event) => {
  file.value = event.target.files[0];
  error.value = null;
};

const uploadFile = async () => {
  if (!file.value) {
    alert("Please select a file first.");
    return;
  }

  loading.value = true;
  error.value = null;

  const formData = new FormData();
  formData.append("file", file.value);

  try {
    const response = await axios.post(`${BASE_URL}/upload`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    analytics.value = response.data;
    console.log("Analytics data received:", analytics.value);
  } catch (err) {
    error.value =
      err.response?.data?.message || "File upload failed. Please try again.";
    analytics.value = null;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.file-upload {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
}

.analytics-dashboard {
  margin-top: 30px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.stat-card p {
  margin: 10px 0 0;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.chart-container {
  margin-top: 30px;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 400px;
}

.chart-container h2 {
  margin-bottom: 20px;
  color: #333;
}

input[type="file"] {
  margin: 10px 0;
}

button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #d6d6d6;
  cursor: not-allowed;
}

.loading {
  margin-top: 20px;
  font-size: 16px;
  color: #555;
}

.error {
  margin-top: 20px;
  color: red;
  font-weight: bold;
}
.chart-navbar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.chart-navbar button {
  padding: 0.5rem 1rem;
  border: blac;
  background: #844747;
  cursor: pointer;
  border-radius: 5px;
}

.chart-navbar button.active {
  background: #007bff;
  color: white;
}

.chart-container {
  margin-top: 1rem;
}
.chart-wrapper {
  position: relative;
  height: 300px; /* Adjust this value to control chart height */
  width: 100%;
}
</style>
