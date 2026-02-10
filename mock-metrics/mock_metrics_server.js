#!/usr/bin/env node

const express = require("express");
const app = express();
const PORT = 9200;

const randInt = (min, max) =>
  Math.floor(Math.random() * (max - min + 1)) + min;

const randFloat = (min, max, d = 2) =>
  Number((Math.random() * (max - min) + min).toFixed(d));

app.get("/metrics-json", (req, res) => {

  const cpu = randInt(50, 95);
  const memory = randInt(30, 85);
  const temp = randInt(40, 75);

  const load = (cpu + memory + temp) / 3;

  const efficiency = Math.max(0.2, Math.min(1, 1 - load / 120));

  const baselineKwh = 2500;
  const reductionPercent = Math.round(30 * efficiency);
  const currentKwh = Math.round(
    baselineKwh * (1 - reductionPercent / 100)
  );

  const costPerKwh = 0.10;
  const monthlySavings = Number(
    (baselineKwh - currentKwh) * costPerKwh
  ).toFixed(2);

  const co2PerKwh = 0.4;
  const co2ReductionKg = Number(
    (baselineKwh - currentKwh) * co2PerKwh
  ).toFixed(2);

  res.json({
    energy: {
      reduction_percent: reductionPercent,
      baseline_kwh: baselineKwh,
      current_kwh: currentKwh,
      target_reduction_percent: 20
    },

    cost_savings: {
      monthly_savings: Number(monthlySavings),
      min_savings: 20,
      max_savings: 40,
      cost_per_kwh: costPerKwh
    },

    co2_reduction: {
      monthly_reduction_kg: Number(co2ReductionKg),
      co2_per_kwh: co2PerKwh,
      trees_equivalent: Number((co2ReductionKg / 21).toFixed(2))
    },

    security: {
      threats_detected: randInt(0, 5),
      threats_blocked: randInt(0, 5),
      requests_scanned: randInt(10000, 20000),
      accuracy_percent: randFloat(95, 99.9)
    },

    servers: {
      total_monitored: 5,
      online: randInt(3, 5),
      in_sleep_mode: randInt(0, 2),
      avg_cpu_percent: cpu,
      avg_memory_percent: memory,
      avg_temperature_celsius: temp
    },

    thresholds: {
      cpu_warning: 80,
      cpu_critical: 95,
      memory_warning: 85,
      temperature_warning: 70
    }
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Mock JSON server running → http://0.0.0.0:${PORT}/metrics-json`);
});

