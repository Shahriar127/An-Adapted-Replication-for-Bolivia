# Sensitivity analysis — Bolivia EH 2005

Metrics follow published Table 2 (McBride & Nichols 2018, p.534): PA, UC, LE and BPAC use the denominator TP+FN. Mean of 1000 bootstrap re-draws of the test sample, 95% percentile CI in brackets.
Seed 42. `paper` = overlapping N/2 bootstrap split; `disjoint` = untouched 50/50 test set.

## Protocol: paper

### Threshold 189.09 (full-sample P24.2) — test poverty rate 23.25%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.488 [0.443, 0.532] | 0.512 [0.468, 0.557] | 0.203 [0.162, 0.251] | 0.178 [0.078, 0.276] |
| RandomForest | 0.481 [0.435, 0.523] | 0.519 [0.477, 0.565] | 0.112 [0.082, 0.143] | 0.074 [-0.028, 0.172] |
| IRIS_Q42 | 0.633 [0.589, 0.676] | 0.367 [0.324, 0.411] | 0.324 [0.265, 0.387] | 0.586 [0.486, 0.657] |
| QRF(q=0.40) fixed | 0.712 [0.670, 0.753] | 0.288 [0.247, 0.330] | 0.327 [0.271, 0.387] | 0.667 [0.610, 0.715] |
| QRF(q=0.41) fixed | 0.707 [0.663, 0.746] | 0.293 [0.254, 0.337] | 0.314 [0.260, 0.371] | 0.673 [0.614, 0.722] |
| QRF(q=0.45) fixed | 0.667 [0.623, 0.709] | 0.333 [0.291, 0.377] | 0.244 [0.198, 0.294] | 0.578 [0.469, 0.674] |
| SE OOB-selected (QRF(0.43)) | 0.688 [0.642, 0.729] | 0.312 [0.271, 0.358] | 0.289 [0.237, 0.344] | 0.653 [0.558, 0.713] |
| QRF test-selected (q=0.42) | 0.694 [0.649, 0.735] | 0.306 [0.265, 0.351] | 0.299 [0.246, 0.355] | 0.665 [0.583, 0.716] |

### Threshold 188.77 (full-sample P24.03, published Table 3) — test poverty rate 23.01%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.457 [0.415, 0.499] | 0.543 [0.501, 0.585] | 0.199 [0.158, 0.246] | 0.112 [0.016, 0.211] |
| RandomForest | 0.476 [0.428, 0.520] | 0.524 [0.480, 0.572] | 0.117 [0.088, 0.148] | 0.068 [-0.031, 0.165] |
| IRIS_Q42 | 0.634 [0.589, 0.677] | 0.366 [0.323, 0.411] | 0.334 [0.274, 0.395] | 0.593 [0.494, 0.660] |
| QRF(q=0.40) fixed | 0.713 [0.671, 0.752] | 0.287 [0.248, 0.329] | 0.328 [0.272, 0.387] | 0.667 [0.605, 0.716] |
| QRF(q=0.41) fixed | 0.702 [0.658, 0.742] | 0.298 [0.258, 0.342] | 0.319 [0.265, 0.381] | 0.668 [0.608, 0.715] |
| QRF(q=0.45) fixed | 0.663 [0.619, 0.705] | 0.337 [0.295, 0.381] | 0.251 [0.204, 0.301] | 0.577 [0.471, 0.676] |
| SE OOB-selected (QRF(0.43)) | 0.689 [0.644, 0.729] | 0.311 [0.271, 0.356] | 0.294 [0.242, 0.348] | 0.657 [0.565, 0.713] |
| QRF test-selected (q=0.42) | 0.695 [0.651, 0.736] | 0.305 [0.264, 0.349] | 0.309 [0.256, 0.367] | 0.666 [0.595, 0.714] |

### Threshold 189.05 (IRIS recon., official ~320 Bs) — test poverty rate 23.20%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.489 [0.444, 0.532] | 0.511 [0.468, 0.556] | 0.203 [0.162, 0.251] | 0.181 [0.081, 0.279] |
| RandomForest | 0.482 [0.437, 0.524] | 0.518 [0.476, 0.563] | 0.112 [0.082, 0.143] | 0.076 [-0.025, 0.174] |
| IRIS_Q42 | 0.635 [0.591, 0.677] | 0.365 [0.323, 0.409] | 0.325 [0.265, 0.388] | 0.589 [0.489, 0.660] |
| QRF(q=0.40) fixed | 0.713 [0.672, 0.753] | 0.287 [0.247, 0.328] | 0.327 [0.271, 0.388] | 0.667 [0.609, 0.716] |
| QRF(q=0.41) fixed | 0.709 [0.665, 0.748] | 0.291 [0.252, 0.335] | 0.315 [0.261, 0.372] | 0.674 [0.616, 0.721] |
| QRF(q=0.45) fixed | 0.668 [0.625, 0.709] | 0.332 [0.291, 0.375] | 0.245 [0.198, 0.294] | 0.581 [0.475, 0.676] |
| SE OOB-selected (QRF(0.43)) | 0.689 [0.644, 0.730] | 0.311 [0.270, 0.356] | 0.289 [0.238, 0.345] | 0.655 [0.561, 0.715] |
| QRF test-selected (q=0.42) | 0.696 [0.650, 0.736] | 0.304 [0.264, 0.350] | 0.300 [0.247, 0.356] | 0.666 [0.586, 0.717] |

### Threshold 194.10 (IRIS recon., official ~328 Bs) — test poverty rate 24.62%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.495 [0.452, 0.536] | 0.505 [0.464, 0.548] | 0.194 [0.156, 0.239] | 0.183 [0.086, 0.275] |
| RandomForest | 0.482 [0.440, 0.528] | 0.518 [0.472, 0.560] | 0.106 [0.079, 0.135] | 0.071 [-0.022, 0.163] |
| IRIS_Q42 | 0.648 [0.605, 0.689] | 0.352 [0.311, 0.395] | 0.285 [0.233, 0.342] | 0.579 [0.475, 0.669] |
| QRF(q=0.40) fixed | 0.726 [0.684, 0.766] | 0.274 [0.234, 0.316] | 0.305 [0.254, 0.360] | 0.687 [0.634, 0.731] |
| QRF(q=0.41) fixed | 0.714 [0.672, 0.753] | 0.286 [0.247, 0.328] | 0.287 [0.236, 0.342] | 0.686 [0.616, 0.734] |
| QRF(q=0.45) fixed | 0.674 [0.629, 0.715] | 0.326 [0.285, 0.371] | 0.255 [0.208, 0.305] | 0.602 [0.502, 0.695] |
| SE OOB-selected (QRF(0.45)) | 0.674 [0.629, 0.715] | 0.326 [0.285, 0.371] | 0.255 [0.208, 0.305] | 0.602 [0.502, 0.695] |
| QRF test-selected (q=0.41) | 0.714 [0.672, 0.753] | 0.286 [0.247, 0.328] | 0.287 [0.236, 0.342] | 0.686 [0.616, 0.734] |

### Threshold train-sample P24.2 — test poverty rate 22.22%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.440 [0.398, 0.483] | 0.560 [0.517, 0.602] | 0.188 [0.146, 0.235] | 0.068 [-0.029, 0.169] |
| RandomForest | 0.466 [0.422, 0.510] | 0.534 [0.490, 0.578] | 0.115 [0.084, 0.147] | 0.047 [-0.050, 0.148] |
| IRIS_Q42 | 0.625 [0.581, 0.669] | 0.375 [0.331, 0.419] | 0.328 [0.267, 0.394] | 0.574 [0.467, 0.649] |
| QRF(q=0.40) fixed | 0.700 [0.656, 0.741] | 0.300 [0.259, 0.344] | 0.328 [0.268, 0.393] | 0.662 [0.601, 0.711] |
| QRF(q=0.41) fixed | 0.696 [0.653, 0.738] | 0.304 [0.262, 0.347] | 0.317 [0.261, 0.379] | 0.664 [0.599, 0.713] |
| QRF(q=0.45) fixed | 0.658 [0.614, 0.701] | 0.342 [0.299, 0.386] | 0.244 [0.194, 0.297] | 0.560 [0.455, 0.662] |
| SE OOB-selected (QRF(0.43)) | 0.685 [0.642, 0.727] | 0.315 [0.273, 0.358] | 0.295 [0.241, 0.352] | 0.651 [0.561, 0.708] |
| QRF test-selected (q=0.42) | 0.693 [0.652, 0.735] | 0.307 [0.265, 0.348] | 0.308 [0.253, 0.367] | 0.664 [0.592, 0.713] |

## Protocol: disjoint

### Threshold 189.09 (full-sample P24.2) — test poverty rate 23.25%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.404 [0.363, 0.445] | 0.596 [0.555, 0.637] | 0.150 [0.114, 0.190] | -0.042 [-0.131, 0.044] |
| RandomForest | 0.421 [0.376, 0.466] | 0.579 [0.534, 0.624] | 0.109 [0.080, 0.144] | -0.049 [-0.142, 0.043] |
| IRIS_Q42 | 0.624 [0.578, 0.665] | 0.376 [0.335, 0.422] | 0.263 [0.211, 0.318] | 0.510 [0.407, 0.612] |
| QRF(q=0.40) fixed | 0.666 [0.625, 0.707] | 0.334 [0.293, 0.375] | 0.359 [0.302, 0.424] | 0.630 [0.571, 0.677] |
| QRF(q=0.41) fixed | 0.651 [0.608, 0.692] | 0.349 [0.308, 0.392] | 0.342 [0.287, 0.402] | 0.621 [0.541, 0.674] |
| QRF(q=0.45) fixed | 0.611 [0.569, 0.654] | 0.389 [0.346, 0.431] | 0.283 [0.230, 0.339] | 0.505 [0.403, 0.604] |
| SE OOB-selected (QRF(0.40)) | 0.666 [0.625, 0.707] | 0.334 [0.293, 0.375] | 0.359 [0.302, 0.424] | 0.630 [0.571, 0.677] |
| QRF test-selected (q=0.40) | 0.666 [0.625, 0.707] | 0.334 [0.293, 0.375] | 0.359 [0.302, 0.424] | 0.630 [0.571, 0.677] |

### Threshold 188.77 (full-sample P24.03, published Table 3) — test poverty rate 23.15%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.403 [0.364, 0.446] | 0.597 [0.554, 0.636] | 0.153 [0.117, 0.194] | -0.041 [-0.128, 0.046] |
| RandomForest | 0.421 [0.375, 0.466] | 0.579 [0.534, 0.625] | 0.110 [0.080, 0.145] | -0.049 [-0.141, 0.045] |
| IRIS_Q42 | 0.626 [0.581, 0.668] | 0.374 [0.332, 0.419] | 0.262 [0.211, 0.317] | 0.514 [0.413, 0.615] |
| QRF(q=0.40) fixed | 0.658 [0.615, 0.699] | 0.342 [0.301, 0.385] | 0.354 [0.297, 0.419] | 0.627 [0.562, 0.676] |
| QRF(q=0.41) fixed | 0.645 [0.603, 0.687] | 0.355 [0.313, 0.397] | 0.337 [0.281, 0.399] | 0.612 [0.525, 0.673] |
| QRF(q=0.45) fixed | 0.603 [0.561, 0.646] | 0.397 [0.354, 0.439] | 0.278 [0.227, 0.333] | 0.484 [0.388, 0.590] |
| SE OOB-selected (QRF(0.40)) | 0.658 [0.615, 0.699] | 0.342 [0.301, 0.385] | 0.354 [0.297, 0.419] | 0.627 [0.562, 0.676] |
| QRF test-selected (q=0.40) | 0.658 [0.615, 0.699] | 0.342 [0.301, 0.385] | 0.354 [0.297, 0.419] | 0.627 [0.562, 0.676] |

### Threshold 189.05 (IRIS recon., official ~320 Bs) — test poverty rate 23.20%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.405 [0.364, 0.447] | 0.595 [0.553, 0.636] | 0.150 [0.114, 0.190] | -0.040 [-0.128, 0.046] |
| RandomForest | 0.422 [0.376, 0.467] | 0.578 [0.533, 0.624] | 0.110 [0.080, 0.144] | -0.047 [-0.140, 0.044] |
| IRIS_Q42 | 0.625 [0.580, 0.667] | 0.375 [0.333, 0.420] | 0.263 [0.211, 0.319] | 0.513 [0.411, 0.613] |
| QRF(q=0.40) fixed | 0.667 [0.625, 0.708] | 0.333 [0.292, 0.375] | 0.360 [0.303, 0.425] | 0.630 [0.570, 0.678] |
| QRF(q=0.41) fixed | 0.652 [0.610, 0.693] | 0.348 [0.307, 0.390] | 0.343 [0.287, 0.403] | 0.622 [0.541, 0.674] |
| QRF(q=0.45) fixed | 0.612 [0.570, 0.655] | 0.388 [0.345, 0.430] | 0.283 [0.231, 0.340] | 0.508 [0.407, 0.608] |
| SE OOB-selected (QRF(0.40)) | 0.667 [0.625, 0.708] | 0.333 [0.292, 0.375] | 0.360 [0.303, 0.425] | 0.630 [0.570, 0.678] |
| QRF test-selected (q=0.41) | 0.652 [0.610, 0.693] | 0.348 [0.307, 0.390] | 0.343 [0.287, 0.403] | 0.622 [0.541, 0.674] |

### Threshold 194.10 (IRIS recon., official ~328 Bs) — test poverty rate 24.23%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.422 [0.382, 0.464] | 0.578 [0.536, 0.618] | 0.142 [0.108, 0.179] | -0.015 [-0.101, 0.074] |
| RandomForest | 0.441 [0.395, 0.484] | 0.559 [0.516, 0.605] | 0.107 [0.079, 0.138] | -0.012 [-0.104, 0.077] |
| IRIS_Q42 | 0.631 [0.587, 0.670] | 0.369 [0.330, 0.413] | 0.250 [0.204, 0.303] | 0.511 [0.417, 0.610] |
| QRF(q=0.40) fixed | 0.682 [0.642, 0.720] | 0.318 [0.280, 0.358] | 0.330 [0.278, 0.392] | 0.652 [0.591, 0.697] |
| QRF(q=0.41) fixed | 0.669 [0.630, 0.709] | 0.331 [0.291, 0.370] | 0.314 [0.263, 0.373] | 0.638 [0.556, 0.693] |
| QRF(q=0.45) fixed | 0.619 [0.580, 0.660] | 0.381 [0.340, 0.420] | 0.261 [0.214, 0.314] | 0.499 [0.398, 0.595] |
| SE OOB-selected (QRF(0.40)) | 0.682 [0.642, 0.720] | 0.318 [0.280, 0.358] | 0.330 [0.278, 0.392] | 0.652 [0.591, 0.697] |
| QRF test-selected (q=0.40) | 0.682 [0.642, 0.720] | 0.318 [0.280, 0.358] | 0.330 [0.278, 0.392] | 0.652 [0.591, 0.697] |

### Threshold train-sample P24.2 — test poverty rate 22.52%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.413 [0.372, 0.457] | 0.587 [0.543, 0.628] | 0.159 [0.121, 0.201] | -0.016 [-0.105, 0.077] |
| RandomForest | 0.413 [0.365, 0.457] | 0.587 [0.543, 0.635] | 0.104 [0.075, 0.137] | -0.070 [-0.164, 0.021] |
| IRIS_Q42 | 0.611 [0.567, 0.652] | 0.389 [0.348, 0.433] | 0.271 [0.219, 0.327] | 0.494 [0.395, 0.595] |
| QRF(q=0.40) fixed | 0.651 [0.607, 0.694] | 0.349 [0.306, 0.393] | 0.357 [0.300, 0.421] | 0.620 [0.550, 0.669] |
| QRF(q=0.41) fixed | 0.640 [0.597, 0.683] | 0.360 [0.317, 0.403] | 0.344 [0.286, 0.411] | 0.607 [0.522, 0.666] |
| QRF(q=0.45) fixed | 0.600 [0.558, 0.646] | 0.400 [0.354, 0.442] | 0.288 [0.234, 0.346] | 0.488 [0.390, 0.598] |
| SE OOB-selected (QRF(0.39)) | 0.659 [0.616, 0.701] | 0.341 [0.299, 0.384] | 0.366 [0.306, 0.433] | 0.622 [0.556, 0.670] |
| QRF test-selected (q=0.40) | 0.651 [0.607, 0.694] | 0.349 [0.306, 0.393] | 0.357 [0.300, 0.421] | 0.620 [0.550, 0.669] |

## Step 2 — paired difference QRF(40) − QRF(45)

| Protocol | Threshold | Metric | Diff | 95% CI | CI excludes 0 |
|---|---|---|---|---|---|
| paper | 189.09 (full-sample P24.2) | PA | +0.0448 | [+0.0263, +0.0649] | yes |
| paper | 189.09 (full-sample P24.2) | UC | -0.0448 | [-0.0649, -0.0263] | yes |
| paper | 189.09 (full-sample P24.2) | LE | +0.0826 | [+0.0575, +0.1096] | yes |
| paper | 189.09 (full-sample P24.2) | BPAC | +0.0897 | [-0.0478, +0.1869] | no |
| paper | 188.77 (full-sample P24.03, published Table 3) | PA | +0.0496 | [+0.0301, +0.0710] | yes |
| paper | 188.77 (full-sample P24.03, published Table 3) | UC | -0.0496 | [-0.0710, -0.0301] | yes |
| paper | 188.77 (full-sample P24.03, published Table 3) | LE | +0.0771 | [+0.0528, +0.1020] | yes |
| paper | 188.77 (full-sample P24.03, published Table 3) | BPAC | +0.0893 | [-0.0441, +0.1894] | no |
| paper | 189.05 (IRIS recon., official ~320 Bs) | PA | +0.0449 | [+0.0263, +0.0651] | yes |
| paper | 189.05 (IRIS recon., official ~320 Bs) | UC | -0.0449 | [-0.0651, -0.0263] | yes |
| paper | 189.05 (IRIS recon., official ~320 Bs) | LE | +0.0828 | [+0.0576, +0.1096] | yes |
| paper | 189.05 (IRIS recon., official ~320 Bs) | BPAC | +0.0863 | [-0.0511, +0.1864] | no |
| paper | 194.10 (IRIS recon., official ~328 Bs) | PA | +0.0520 | [+0.0333, +0.0738] | yes |
| paper | 194.10 (IRIS recon., official ~328 Bs) | UC | -0.0520 | [-0.0738, -0.0333] | yes |
| paper | 194.10 (IRIS recon., official ~328 Bs) | LE | +0.0499 | [+0.0309, +0.0700] | yes |
| paper | 194.10 (IRIS recon., official ~328 Bs) | BPAC | +0.0848 | [-0.0392, +0.1718] | no |
| paper | train-sample P24.2 | PA | +0.0422 | [+0.0247, +0.0626] | yes |
| paper | train-sample P24.2 | UC | -0.0422 | [-0.0626, -0.0247] | yes |
| paper | train-sample P24.2 | LE | +0.0840 | [+0.0569, +0.1114] | yes |
| paper | train-sample P24.2 | BPAC | +0.1015 | [-0.0315, +0.1903] | no |
| disjoint | 189.09 (full-sample P24.2) | PA | +0.0549 | [+0.0358, +0.0763] | yes |
| disjoint | 189.09 (full-sample P24.2) | UC | -0.0549 | [-0.0763, -0.0358] | yes |
| disjoint | 189.09 (full-sample P24.2) | LE | +0.0760 | [+0.0516, +0.1046] | yes |
| disjoint | 189.09 (full-sample P24.2) | BPAC | +0.1256 | [-0.0148, +0.2054] | no |
| disjoint | 188.77 (full-sample P24.03, published Table 3) | PA | +0.0549 | [+0.0352, +0.0750] | yes |
| disjoint | 188.77 (full-sample P24.03, published Table 3) | UC | -0.0549 | [-0.0750, -0.0352] | yes |
| disjoint | 188.77 (full-sample P24.03, published Table 3) | LE | +0.0765 | [+0.0526, +0.1026] | yes |
| disjoint | 188.77 (full-sample P24.03, published Table 3) | BPAC | +0.1432 | [+0.0125, +0.2149] | yes |
| disjoint | 189.05 (IRIS recon., official ~320 Bs) | PA | +0.0551 | [+0.0360, +0.0766] | yes |
| disjoint | 189.05 (IRIS recon., official ~320 Bs) | UC | -0.0551 | [-0.0766, -0.0360] | yes |
| disjoint | 189.05 (IRIS recon., official ~320 Bs) | LE | +0.0761 | [+0.0518, +0.1048] | yes |
| disjoint | 189.05 (IRIS recon., official ~320 Bs) | BPAC | +0.1228 | [-0.0194, +0.2047] | no |
| disjoint | 194.10 (IRIS recon., official ~328 Bs) | PA | +0.0628 | [+0.0420, +0.0840] | yes |
| disjoint | 194.10 (IRIS recon., official ~328 Bs) | UC | -0.0628 | [-0.0840, -0.0420] | yes |
| disjoint | 194.10 (IRIS recon., official ~328 Bs) | LE | +0.0685 | [+0.0449, +0.0946] | yes |
| disjoint | 194.10 (IRIS recon., official ~328 Bs) | BPAC | +0.1536 | [+0.0323, +0.2257] | yes |
| disjoint | train-sample P24.2 | PA | +0.0501 | [+0.0308, +0.0704] | yes |
| disjoint | train-sample P24.2 | UC | -0.0501 | [-0.0704, -0.0308] | yes |
| disjoint | train-sample P24.2 | LE | +0.0698 | [+0.0459, +0.0943] | yes |
| disjoint | train-sample P24.2 | BPAC | +0.1314 | [-0.0000, +0.2008] | no |

## Step 3 — paired difference vs 189.09 Bs (same model, same test resamples)

| Protocol | Model | Change | Metric | Diff | 95% CI | CI excludes 0 |
|---|---|---|---|---|---|---|
| paper | DecisionTree | 188.77 − 189.09 | PA | -0.0309 | [-0.0480, -0.0150] | yes |
| paper | DecisionTree | 188.77 − 189.09 | UC | +0.0309 | [+0.0150, +0.0480] | yes |
| paper | DecisionTree | 188.77 − 189.09 | LE | -0.0043 | [-0.0159, +0.0079] | no |
| paper | DecisionTree | 188.77 − 189.09 | BPAC | -0.0660 | [-0.1021, -0.0336] | yes |
| paper | RandomForest | 188.77 − 189.09 | PA | -0.0055 | [-0.0137, +0.0010] | no |
| paper | RandomForest | 188.77 − 189.09 | UC | +0.0055 | [-0.0010, +0.0137] | no |
| paper | RandomForest | 188.77 − 189.09 | LE | +0.0052 | [-0.0038, +0.0150] | no |
| paper | RandomForest | 188.77 − 189.09 | BPAC | -0.0059 | [-0.0196, +0.0068] | no |
| paper | IRIS_Q42 | 188.77 − 189.09 | PA | +0.0004 | [-0.0038, +0.0052] | no |
| paper | IRIS_Q42 | 188.77 − 189.09 | UC | -0.0004 | [-0.0052, +0.0038] | no |
| paper | IRIS_Q42 | 188.77 − 189.09 | LE | +0.0097 | [+0.0012, +0.0210] | yes |
| paper | IRIS_Q42 | 188.77 − 189.09 | BPAC | +0.0070 | [-0.0156, +0.0201] | no |
| paper | QRF(q=0.40) fixed | 188.77 − 189.09 | PA | +0.0012 | [-0.0028, +0.0062] | no |
| paper | QRF(q=0.40) fixed | 188.77 − 189.09 | UC | -0.0012 | [-0.0062, +0.0028] | no |
| paper | QRF(q=0.40) fixed | 188.77 − 189.09 | LE | +0.0013 | [-0.0109, +0.0146] | no |
| paper | QRF(q=0.40) fixed | 188.77 − 189.09 | BPAC | -0.0007 | [-0.0138, +0.0116] | no |
| paper | QRF(q=0.41) fixed | 188.77 − 189.09 | PA | -0.0054 | [-0.0146, +0.0027] | no |
| paper | QRF(q=0.41) fixed | 188.77 − 189.09 | UC | +0.0054 | [-0.0027, +0.0146] | no |
| paper | QRF(q=0.41) fixed | 188.77 − 189.09 | LE | +0.0054 | [-0.0054, +0.0175] | no |
| paper | QRF(q=0.41) fixed | 188.77 − 189.09 | BPAC | -0.0056 | [-0.0209, +0.0071] | no |
| paper | QRF(q=0.45) fixed | 188.77 − 189.09 | PA | -0.0035 | [-0.0112, +0.0035] | no |
| paper | QRF(q=0.45) fixed | 188.77 − 189.09 | UC | +0.0035 | [-0.0035, +0.0112] | no |
| paper | QRF(q=0.45) fixed | 188.77 − 189.09 | LE | +0.0068 | [-0.0019, +0.0179] | no |
| paper | QRF(q=0.45) fixed | 188.77 − 189.09 | BPAC | -0.0003 | [-0.0173, +0.0158] | no |
| paper | SE OOB-selected | 188.77 − 189.09 | PA | +0.0010 | [-0.0031, +0.0059] | no |
| paper | SE OOB-selected | 188.77 − 189.09 | UC | -0.0010 | [-0.0059, +0.0031] | no |
| paper | SE OOB-selected | 188.77 − 189.09 | LE | +0.0052 | [-0.0051, +0.0171] | no |
| paper | SE OOB-selected | 188.77 − 189.09 | BPAC | +0.0035 | [-0.0126, +0.0181] | no |
| paper | QRF test-selected | 188.77 − 189.09 | PA | +0.0011 | [-0.0031, +0.0060] | no |
| paper | QRF test-selected | 188.77 − 189.09 | UC | -0.0011 | [-0.0060, +0.0031] | no |
| paper | QRF test-selected | 188.77 − 189.09 | LE | +0.0094 | [+0.0011, +0.0204] | yes |
| paper | QRF test-selected | 188.77 − 189.09 | BPAC | +0.0010 | [-0.0179, +0.0198] | no |
| paper | DecisionTree | 189.05 − 189.09 | PA | +0.0010 | [+0.0000, +0.0032] | no |
| paper | DecisionTree | 189.05 − 189.09 | UC | -0.0010 | [-0.0032, +0.0000] | no |
| paper | DecisionTree | 189.05 − 189.09 | LE | +0.0004 | [+0.0000, +0.0014] | no |
| paper | DecisionTree | 189.05 − 189.09 | BPAC | +0.0025 | [+0.0000, +0.0078] | no |
| paper | RandomForest | 189.05 − 189.09 | PA | +0.0010 | [+0.0000, +0.0032] | no |
| paper | RandomForest | 189.05 − 189.09 | UC | -0.0010 | [-0.0032, +0.0000] | no |
| paper | RandomForest | 189.05 − 189.09 | LE | +0.0002 | [+0.0000, +0.0008] | no |
| paper | RandomForest | 189.05 − 189.09 | BPAC | +0.0023 | [+0.0000, +0.0071] | no |
| paper | IRIS_Q42 | 189.05 − 189.09 | PA | +0.0013 | [+0.0000, +0.0041] | no |
| paper | IRIS_Q42 | 189.05 − 189.09 | UC | -0.0013 | [-0.0041, +0.0000] | no |
| paper | IRIS_Q42 | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0022] | no |
| paper | IRIS_Q42 | 189.05 − 189.09 | BPAC | +0.0029 | [-0.0010, +0.0103] | no |
| paper | QRF(q=0.40) fixed | 189.05 − 189.09 | PA | +0.0015 | [+0.0000, +0.0046] | no |
| paper | QRF(q=0.40) fixed | 189.05 − 189.09 | UC | -0.0015 | [-0.0046, +0.0000] | no |
| paper | QRF(q=0.40) fixed | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0022] | no |
| paper | QRF(q=0.40) fixed | 189.05 − 189.09 | BPAC | -0.0001 | [-0.0022, +0.0068] | no |
| paper | QRF(q=0.41) fixed | 189.05 − 189.09 | PA | +0.0015 | [+0.0000, +0.0046] | no |
| paper | QRF(q=0.41) fixed | 189.05 − 189.09 | UC | -0.0015 | [-0.0046, +0.0000] | no |
| paper | QRF(q=0.41) fixed | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0021] | no |
| paper | QRF(q=0.41) fixed | 189.05 − 189.09 | BPAC | +0.0005 | [-0.0021, +0.0071] | no |
| paper | QRF(q=0.45) fixed | 189.05 − 189.09 | PA | +0.0014 | [+0.0000, +0.0044] | no |
| paper | QRF(q=0.45) fixed | 189.05 − 189.09 | UC | -0.0014 | [-0.0044, +0.0000] | no |
| paper | QRF(q=0.45) fixed | 189.05 − 189.09 | LE | +0.0005 | [+0.0000, +0.0017] | no |
| paper | QRF(q=0.45) fixed | 189.05 − 189.09 | BPAC | +0.0034 | [+0.0000, +0.0105] | no |
| paper | SE OOB-selected | 189.05 − 189.09 | PA | +0.0015 | [+0.0000, +0.0045] | no |
| paper | SE OOB-selected | 189.05 − 189.09 | UC | -0.0015 | [-0.0045, +0.0000] | no |
| paper | SE OOB-selected | 189.05 − 189.09 | LE | +0.0006 | [+0.0000, +0.0020] | no |
| paper | SE OOB-selected | 189.05 − 189.09 | BPAC | +0.0024 | [-0.0015, +0.0104] | no |
| paper | QRF test-selected | 189.05 − 189.09 | PA | +0.0015 | [+0.0000, +0.0045] | no |
| paper | QRF test-selected | 189.05 − 189.09 | UC | -0.0015 | [-0.0045, +0.0000] | no |
| paper | QRF test-selected | 189.05 − 189.09 | LE | +0.0006 | [+0.0000, +0.0021] | no |
| paper | QRF test-selected | 189.05 − 189.09 | BPAC | +0.0017 | [-0.0018, +0.0103] | no |
| paper | DecisionTree | 194.10 − 189.09 | PA | +0.0069 | [-0.0093, +0.0234] | no |
| paper | DecisionTree | 194.10 − 189.09 | UC | -0.0069 | [-0.0234, +0.0093] | no |
| paper | DecisionTree | 194.10 − 189.09 | LE | -0.0091 | [-0.0279, +0.0082] | no |
| paper | DecisionTree | 194.10 − 189.09 | BPAC | +0.0047 | [-0.0296, +0.0391] | no |
| paper | RandomForest | 194.10 − 189.09 | PA | +0.0012 | [-0.0144, +0.0167] | no |
| paper | RandomForest | 194.10 − 189.09 | UC | -0.0012 | [-0.0167, +0.0144] | no |
| paper | RandomForest | 194.10 − 189.09 | LE | -0.0059 | [-0.0194, +0.0076] | no |
| paper | RandomForest | 194.10 − 189.09 | BPAC | -0.0035 | [-0.0346, +0.0297] | no |
| paper | IRIS_Q42 | 194.10 − 189.09 | PA | +0.0143 | [+0.0009, +0.0301] | yes |
| paper | IRIS_Q42 | 194.10 − 189.09 | UC | -0.0143 | [-0.0301, -0.0009] | yes |
| paper | IRIS_Q42 | 194.10 − 189.09 | LE | -0.0392 | [-0.0689, -0.0126] | yes |
| paper | IRIS_Q42 | 194.10 − 189.09 | BPAC | -0.0064 | [-0.0421, +0.0408] | no |
| paper | QRF(q=0.40) fixed | 194.10 − 189.09 | PA | +0.0141 | [-0.0056, +0.0322] | no |
| paper | QRF(q=0.40) fixed | 194.10 − 189.09 | UC | -0.0141 | [-0.0322, +0.0056] | no |
| paper | QRF(q=0.40) fixed | 194.10 − 189.09 | LE | -0.0214 | [-0.0470, +0.0026] | no |
| paper | QRF(q=0.40) fixed | 194.10 − 189.09 | BPAC | +0.0198 | [-0.0091, +0.0470] | no |
| paper | QRF(q=0.41) fixed | 194.10 − 189.09 | PA | +0.0064 | [-0.0096, +0.0227] | no |
| paper | QRF(q=0.41) fixed | 194.10 − 189.09 | UC | -0.0064 | [-0.0227, +0.0096] | no |
| paper | QRF(q=0.41) fixed | 194.10 − 189.09 | LE | -0.0266 | [-0.0517, -0.0053] | yes |
| paper | QRF(q=0.41) fixed | 194.10 − 189.09 | BPAC | +0.0128 | [-0.0325, +0.0474] | no |
| paper | QRF(q=0.45) fixed | 194.10 − 189.09 | PA | +0.0069 | [-0.0096, +0.0234] | no |
| paper | QRF(q=0.45) fixed | 194.10 − 189.09 | UC | -0.0069 | [-0.0234, +0.0096] | no |
| paper | QRF(q=0.45) fixed | 194.10 − 189.09 | LE | +0.0113 | [-0.0141, +0.0367] | no |
| paper | QRF(q=0.45) fixed | 194.10 − 189.09 | BPAC | +0.0248 | [-0.0177, +0.0660] | no |
| paper | SE OOB-selected | 194.10 − 189.09 | PA | -0.0143 | [-0.0291, -0.0001] | yes |
| paper | SE OOB-selected | 194.10 − 189.09 | UC | +0.0143 | [+0.0001, +0.0291] | yes |
| paper | SE OOB-selected | 194.10 − 189.09 | LE | -0.0333 | [-0.0563, -0.0116] | yes |
| paper | SE OOB-selected | 194.10 − 189.09 | BPAC | -0.0507 | [-0.0929, +0.0254] | no |
| paper | QRF test-selected | 194.10 − 189.09 | PA | +0.0194 | [+0.0001, +0.0395] | yes |
| paper | QRF test-selected | 194.10 − 189.09 | UC | -0.0194 | [-0.0395, -0.0001] | yes |
| paper | QRF test-selected | 194.10 − 189.09 | LE | -0.0120 | [-0.0356, +0.0114] | no |
| paper | QRF test-selected | 194.10 − 189.09 | BPAC | +0.0214 | [-0.0099, +0.0632] | no |
| paper | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0478 | [-0.0708, -0.0264] | yes |
| paper | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0478 | [+0.0264, +0.0708] | yes |
| paper | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | LE | -0.0149 | [-0.0372, +0.0069] | no |
| paper | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.1105 | [-0.1569, -0.0636] | yes |
| paper | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0152 | [-0.0328, +0.0028] | no |
| paper | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0152 | [-0.0028, +0.0328] | no |
| paper | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0029 | [-0.0087, +0.0146] | no |
| paper | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0275 | [-0.0628, +0.0082] | no |
| paper | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0085 | [-0.0251, +0.0074] | no |
| paper | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0085 | [-0.0074, +0.0251] | no |
| paper | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0042 | [-0.0172, +0.0275] | no |
| paper | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0121 | [-0.0504, +0.0237] | no |
| paper | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0114 | [-0.0262, +0.0022] | no |
| paper | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0114 | [-0.0022, +0.0262] | no |
| paper | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0017 | [-0.0215, +0.0261] | no |
| paper | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0055 | [-0.0354, +0.0200] | no |
| paper | QRF(q=0.41) fixed | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0116 | [-0.0250, +0.0019] | no |
| paper | QRF(q=0.41) fixed | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0116 | [-0.0019, +0.0250] | no |
| paper | QRF(q=0.41) fixed | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0032 | [-0.0195, +0.0267] | no |
| paper | QRF(q=0.41) fixed | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0092 | [-0.0419, +0.0179] | no |
| paper | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0087 | [-0.0237, +0.0053] | no |
| paper | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0087 | [-0.0053, +0.0237] | no |
| paper | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0003 | [-0.0233, +0.0233] | no |
| paper | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0172 | [-0.0530, +0.0181] | no |
| paper | SE OOB-selected | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0034 | [-0.0170, +0.0107] | no |
| paper | SE OOB-selected | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0034 | [-0.0107, +0.0170] | no |
| paper | SE OOB-selected | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0064 | [-0.0142, +0.0292] | no |
| paper | SE OOB-selected | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0024 | [-0.0291, +0.0307] | no |
| paper | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0009 | [-0.0121, +0.0104] | no |
| paper | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0009 | [-0.0104, +0.0121] | no |
| paper | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0089 | [-0.0120, +0.0310] | no |
| paper | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0007 | [-0.0274, +0.0285] | no |
| disjoint | DecisionTree | 188.77 − 189.09 | PA | -0.0005 | [-0.0037, +0.0025] | no |
| disjoint | DecisionTree | 188.77 − 189.09 | UC | +0.0005 | [-0.0025, +0.0037] | no |
| disjoint | DecisionTree | 188.77 − 189.09 | LE | +0.0029 | [+0.0000, +0.0082] | no |
| disjoint | DecisionTree | 188.77 − 189.09 | BPAC | +0.0019 | [-0.0003, +0.0063] | no |
| disjoint | RandomForest | 188.77 − 189.09 | PA | -0.0003 | [-0.0053, +0.0037] | no |
| disjoint | RandomForest | 188.77 − 189.09 | UC | +0.0003 | [-0.0037, +0.0053] | no |
| disjoint | RandomForest | 188.77 − 189.09 | LE | +0.0005 | [+0.0000, +0.0012] | no |
| disjoint | RandomForest | 188.77 − 189.09 | BPAC | -0.0002 | [-0.0104, +0.0083] | no |
| disjoint | IRIS_Q42 | 188.77 − 189.09 | PA | +0.0027 | [+0.0000, +0.0066] | no |
| disjoint | IRIS_Q42 | 188.77 − 189.09 | UC | -0.0027 | [-0.0066, +0.0000] | no |
| disjoint | IRIS_Q42 | 188.77 − 189.09 | LE | -0.0010 | [-0.0059, +0.0024] | no |
| disjoint | IRIS_Q42 | 188.77 − 189.09 | BPAC | +0.0043 | [-0.0043, +0.0148] | no |
| disjoint | QRF(q=0.40) fixed | 188.77 − 189.09 | PA | -0.0080 | [-0.0171, -0.0007] | yes |
| disjoint | QRF(q=0.40) fixed | 188.77 − 189.09 | UC | +0.0080 | [+0.0007, +0.0171] | yes |
| disjoint | QRF(q=0.40) fixed | 188.77 − 189.09 | LE | -0.0046 | [-0.0148, +0.0048] | no |
| disjoint | QRF(q=0.40) fixed | 188.77 − 189.09 | BPAC | -0.0034 | [-0.0326, +0.0144] | no |
| disjoint | QRF(q=0.41) fixed | 188.77 − 189.09 | PA | -0.0060 | [-0.0145, +0.0006] | no |
| disjoint | QRF(q=0.41) fixed | 188.77 − 189.09 | UC | +0.0060 | [-0.0006, +0.0145] | no |
| disjoint | QRF(q=0.41) fixed | 188.77 − 189.09 | LE | -0.0050 | [-0.0159, +0.0047] | no |
| disjoint | QRF(q=0.41) fixed | 188.77 − 189.09 | BPAC | -0.0089 | [-0.0332, +0.0122] | no |
| disjoint | QRF(q=0.45) fixed | 188.77 − 189.09 | PA | -0.0079 | [-0.0172, -0.0003] | yes |
| disjoint | QRF(q=0.45) fixed | 188.77 − 189.09 | UC | +0.0079 | [+0.0003, +0.0172] | yes |
| disjoint | QRF(q=0.45) fixed | 188.77 − 189.09 | LE | -0.0051 | [-0.0151, +0.0046] | no |
| disjoint | QRF(q=0.45) fixed | 188.77 − 189.09 | BPAC | -0.0210 | [-0.0400, -0.0035] | yes |
| disjoint | SE OOB-selected | 188.77 − 189.09 | PA | -0.0080 | [-0.0171, -0.0007] | yes |
| disjoint | SE OOB-selected | 188.77 − 189.09 | UC | +0.0080 | [+0.0007, +0.0171] | yes |
| disjoint | SE OOB-selected | 188.77 − 189.09 | LE | -0.0046 | [-0.0148, +0.0048] | no |
| disjoint | SE OOB-selected | 188.77 − 189.09 | BPAC | -0.0034 | [-0.0326, +0.0144] | no |
| disjoint | QRF test-selected | 188.77 − 189.09 | PA | -0.0080 | [-0.0171, -0.0007] | yes |
| disjoint | QRF test-selected | 188.77 − 189.09 | UC | +0.0080 | [+0.0007, +0.0171] | yes |
| disjoint | QRF test-selected | 188.77 − 189.09 | LE | -0.0046 | [-0.0148, +0.0048] | no |
| disjoint | QRF test-selected | 188.77 − 189.09 | BPAC | -0.0034 | [-0.0326, +0.0144] | no |
| disjoint | DecisionTree | 189.05 − 189.09 | PA | +0.0008 | [+0.0000, +0.0027] | no |
| disjoint | DecisionTree | 189.05 − 189.09 | UC | -0.0008 | [-0.0027, +0.0000] | no |
| disjoint | DecisionTree | 189.05 − 189.09 | LE | +0.0003 | [+0.0000, +0.0010] | no |
| disjoint | DecisionTree | 189.05 − 189.09 | BPAC | +0.0020 | [+0.0000, +0.0064] | no |
| disjoint | RandomForest | 189.05 − 189.09 | PA | +0.0009 | [+0.0000, +0.0028] | no |
| disjoint | RandomForest | 189.05 − 189.09 | UC | -0.0009 | [-0.0028, +0.0000] | no |
| disjoint | RandomForest | 189.05 − 189.09 | LE | +0.0002 | [+0.0000, +0.0007] | no |
| disjoint | RandomForest | 189.05 − 189.09 | BPAC | +0.0020 | [+0.0000, +0.0064] | no |
| disjoint | IRIS_Q42 | 189.05 − 189.09 | PA | +0.0013 | [+0.0000, +0.0041] | no |
| disjoint | IRIS_Q42 | 189.05 − 189.09 | UC | -0.0013 | [-0.0041, +0.0000] | no |
| disjoint | IRIS_Q42 | 189.05 − 189.09 | LE | +0.0005 | [+0.0000, +0.0018] | no |
| disjoint | IRIS_Q42 | 189.05 − 189.09 | BPAC | +0.0031 | [+0.0000, +0.0098] | no |
| disjoint | QRF(q=0.40) fixed | 189.05 − 189.09 | PA | +0.0014 | [+0.0000, +0.0044] | no |
| disjoint | QRF(q=0.40) fixed | 189.05 − 189.09 | UC | -0.0014 | [-0.0044, +0.0000] | no |
| disjoint | QRF(q=0.40) fixed | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0025] | no |
| disjoint | QRF(q=0.40) fixed | 189.05 − 189.09 | BPAC | +0.0003 | [-0.0024, +0.0071] | no |
| disjoint | QRF(q=0.41) fixed | 189.05 − 189.09 | PA | +0.0013 | [+0.0000, +0.0043] | no |
| disjoint | QRF(q=0.41) fixed | 189.05 − 189.09 | UC | -0.0013 | [-0.0043, +0.0000] | no |
| disjoint | QRF(q=0.41) fixed | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0024] | no |
| disjoint | QRF(q=0.41) fixed | 189.05 − 189.09 | BPAC | +0.0016 | [-0.0019, +0.0100] | no |
| disjoint | QRF(q=0.45) fixed | 189.05 − 189.09 | PA | +0.0013 | [+0.0000, +0.0040] | no |
| disjoint | QRF(q=0.45) fixed | 189.05 − 189.09 | UC | -0.0013 | [-0.0040, +0.0000] | no |
| disjoint | QRF(q=0.45) fixed | 189.05 − 189.09 | LE | +0.0006 | [+0.0000, +0.0020] | no |
| disjoint | QRF(q=0.45) fixed | 189.05 − 189.09 | BPAC | +0.0031 | [+0.0000, +0.0100] | no |
| disjoint | SE OOB-selected | 189.05 − 189.09 | PA | +0.0014 | [+0.0000, +0.0044] | no |
| disjoint | SE OOB-selected | 189.05 − 189.09 | UC | -0.0014 | [-0.0044, +0.0000] | no |
| disjoint | SE OOB-selected | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0025] | no |
| disjoint | SE OOB-selected | 189.05 − 189.09 | BPAC | +0.0003 | [-0.0024, +0.0071] | no |
| disjoint | QRF test-selected | 189.05 − 189.09 | PA | -0.0135 | [-0.0260, -0.0032] | yes |
| disjoint | QRF test-selected | 189.05 − 189.09 | UC | +0.0135 | [+0.0032, +0.0260] | yes |
| disjoint | QRF test-selected | 189.05 − 189.09 | LE | -0.0160 | [-0.0284, -0.0054] | yes |
| disjoint | QRF test-selected | 189.05 − 189.09 | BPAC | -0.0078 | [-0.0631, +0.0267] | no |
| disjoint | DecisionTree | 194.10 − 189.09 | PA | +0.0180 | [+0.0026, +0.0335] | yes |
| disjoint | DecisionTree | 194.10 − 189.09 | UC | -0.0180 | [-0.0335, -0.0026] | yes |
| disjoint | DecisionTree | 194.10 − 189.09 | LE | -0.0082 | [-0.0226, +0.0064] | no |
| disjoint | DecisionTree | 194.10 − 189.09 | BPAC | +0.0279 | [-0.0029, +0.0588] | no |
| disjoint | RandomForest | 194.10 − 189.09 | PA | +0.0197 | [+0.0038, +0.0382] | yes |
| disjoint | RandomForest | 194.10 − 189.09 | UC | -0.0197 | [-0.0382, -0.0038] | yes |
| disjoint | RandomForest | 194.10 − 189.09 | LE | -0.0024 | [-0.0175, +0.0121] | no |
| disjoint | RandomForest | 194.10 − 189.09 | BPAC | +0.0369 | [+0.0055, +0.0700] | yes |
| disjoint | IRIS_Q42 | 194.10 − 189.09 | PA | +0.0070 | [-0.0042, +0.0177] | no |
| disjoint | IRIS_Q42 | 194.10 − 189.09 | UC | -0.0070 | [-0.0177, +0.0042] | no |
| disjoint | IRIS_Q42 | 194.10 − 189.09 | LE | -0.0126 | [-0.0353, +0.0092] | no |
| disjoint | IRIS_Q42 | 194.10 − 189.09 | BPAC | +0.0013 | [-0.0246, +0.0296] | no |
| disjoint | QRF(q=0.40) fixed | 194.10 − 189.09 | PA | +0.0157 | [+0.0035, +0.0292] | yes |
| disjoint | QRF(q=0.40) fixed | 194.10 − 189.09 | UC | -0.0157 | [-0.0292, -0.0035] | yes |
| disjoint | QRF(q=0.40) fixed | 194.10 − 189.09 | LE | -0.0290 | [-0.0528, -0.0071] | yes |
| disjoint | QRF(q=0.40) fixed | 194.10 − 189.09 | BPAC | +0.0222 | [-0.0113, +0.0508] | no |
| disjoint | QRF(q=0.41) fixed | 194.10 − 189.09 | PA | +0.0184 | [+0.0047, +0.0327] | yes |
| disjoint | QRF(q=0.41) fixed | 194.10 − 189.09 | UC | -0.0184 | [-0.0327, -0.0047] | yes |
| disjoint | QRF(q=0.41) fixed | 194.10 − 189.09 | LE | -0.0283 | [-0.0514, -0.0066] | yes |
| disjoint | QRF(q=0.41) fixed | 194.10 − 189.09 | BPAC | +0.0171 | [-0.0164, +0.0466] | no |
| disjoint | QRF(q=0.45) fixed | 194.10 − 189.09 | PA | +0.0078 | [-0.0034, +0.0187] | no |
| disjoint | QRF(q=0.45) fixed | 194.10 − 189.09 | UC | -0.0078 | [-0.0187, +0.0034] | no |
| disjoint | QRF(q=0.45) fixed | 194.10 − 189.09 | LE | -0.0215 | [-0.0448, -0.0002] | yes |
| disjoint | QRF(q=0.45) fixed | 194.10 − 189.09 | BPAC | -0.0057 | [-0.0313, +0.0185] | no |
| disjoint | SE OOB-selected | 194.10 − 189.09 | PA | +0.0157 | [+0.0035, +0.0292] | yes |
| disjoint | SE OOB-selected | 194.10 − 189.09 | UC | -0.0157 | [-0.0292, -0.0035] | yes |
| disjoint | SE OOB-selected | 194.10 − 189.09 | LE | -0.0290 | [-0.0528, -0.0071] | yes |
| disjoint | SE OOB-selected | 194.10 − 189.09 | BPAC | +0.0222 | [-0.0113, +0.0508] | no |
| disjoint | QRF test-selected | 194.10 − 189.09 | PA | +0.0157 | [+0.0035, +0.0292] | yes |
| disjoint | QRF test-selected | 194.10 − 189.09 | UC | -0.0157 | [-0.0292, -0.0035] | yes |
| disjoint | QRF test-selected | 194.10 − 189.09 | LE | -0.0290 | [-0.0528, -0.0071] | yes |
| disjoint | QRF test-selected | 194.10 − 189.09 | BPAC | +0.0222 | [-0.0113, +0.0508] | no |
| disjoint | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | PA | +0.0087 | [+0.0021, +0.0156] | yes |
| disjoint | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | UC | -0.0087 | [-0.0156, -0.0021] | yes |
| disjoint | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0092 | [+0.0030, +0.0171] | yes |
| disjoint | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | BPAC | +0.0267 | [+0.0137, +0.0419] | yes |
| disjoint | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0082 | [-0.0224, +0.0056] | no |
| disjoint | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0082 | [-0.0056, +0.0224] | no |
| disjoint | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | LE | -0.0052 | [-0.0170, +0.0045] | no |
| disjoint | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0215 | [-0.0508, +0.0063] | no |
| disjoint | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0122 | [-0.0263, +0.0017] | no |
| disjoint | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0122 | [-0.0017, +0.0263] | no |
| disjoint | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0086 | [-0.0090, +0.0270] | no |
| disjoint | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0157 | [-0.0474, +0.0158] | no |
| disjoint | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0153 | [-0.0315, -0.0013] | yes |
| disjoint | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0153 | [+0.0013, +0.0315] | yes |
| disjoint | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | LE | -0.0015 | [-0.0216, +0.0188] | no |
| disjoint | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0104 | [-0.0560, +0.0174] | no |
| disjoint | QRF(q=0.41) fixed | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0113 | [-0.0274, +0.0028] | no |
| disjoint | QRF(q=0.41) fixed | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0113 | [-0.0028, +0.0274] | no |
| disjoint | QRF(q=0.41) fixed | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0023 | [-0.0165, +0.0209] | no |
| disjoint | QRF(q=0.41) fixed | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0142 | [-0.0472, +0.0122] | no |
| disjoint | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0104 | [-0.0257, +0.0040] | no |
| disjoint | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0104 | [-0.0040, +0.0257] | no |
| disjoint | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0047 | [-0.0119, +0.0212] | no |
| disjoint | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0162 | [-0.0493, +0.0171] | no |
| disjoint | SE OOB-selected | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0066 | [-0.0221, +0.0070] | no |
| disjoint | SE OOB-selected | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0066 | [-0.0070, +0.0221] | no |
| disjoint | SE OOB-selected | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0070 | [-0.0132, +0.0274] | no |
| disjoint | SE OOB-selected | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0078 | [-0.0324, +0.0144] | no |
| disjoint | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0153 | [-0.0315, -0.0013] | yes |
| disjoint | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0153 | [+0.0013, +0.0315] | yes |
| disjoint | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | LE | -0.0015 | [-0.0216, +0.0188] | no |
| disjoint | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0104 | [-0.0560, +0.0174] | no |

## SE model chosen by OOB BPAC, and test-selected quantile (seed 42)

| protocol   | threshold                                      |    line | se_oob_selected   |   q_test_selected |
|:-----------|:-----------------------------------------------|--------:|:------------------|------------------:|
| paper      | 189.09 (full-sample P24.2)                     | 189.091 | QRF(0.43)         |              0.42 |
| paper      | 188.77 (full-sample P24.03, published Table 3) | 188.774 | QRF(0.43)         |              0.42 |
| paper      | 189.05 (IRIS recon., official ~320 Bs)         | 189.05  | QRF(0.43)         |              0.42 |
| paper      | 194.10 (IRIS recon., official ~328 Bs)         | 194.1   | QRF(0.45)         |              0.41 |
| paper      | train-sample P24.2                             | 185.08  | QRF(0.43)         |              0.42 |
| disjoint   | 189.09 (full-sample P24.2)                     | 189.091 | QRF(0.40)         |              0.4  |
| disjoint   | 188.77 (full-sample P24.03, published Table 3) | 188.774 | QRF(0.40)         |              0.4  |
| disjoint   | 189.05 (IRIS recon., official ~320 Bs)         | 189.05  | QRF(0.40)         |              0.41 |
| disjoint   | 194.10 (IRIS recon., official ~328 Bs)         | 194.1   | QRF(0.40)         |              0.4  |
| disjoint   | train-sample P24.2                             | 185.52  | QRF(0.39)         |              0.4  |

## Repeated splits — mean (SD) of point metrics over 30 random splits per protocol

| Protocol | Threshold | Model | PA | UC | LE | BPAC |
|---|---|---|---|---|---|---|
| disjoint | 188.77 | DecisionTree | 0.457 (0.044) | 0.543 (0.044) | 0.184 (0.031) | 0.097 (0.109) |
| disjoint | 188.77 | IRIS_Q42 | 0.611 (0.019) | 0.389 (0.019) | 0.263 (0.023) | 0.485 (0.054) |
| disjoint | 188.77 | QRF test-selected | 0.673 (0.017) | 0.327 (0.017) | 0.334 (0.015) | 0.664 (0.016) |
| disjoint | 188.77 | QRF(q=0.40) fixed | 0.672 (0.022) | 0.328 (0.022) | 0.335 (0.034) | 0.635 (0.035) |
| disjoint | 188.77 | QRF(q=0.41) fixed | 0.659 (0.022) | 0.341 (0.022) | 0.319 (0.031) | 0.619 (0.044) |
| disjoint | 188.77 | QRF(q=0.45) fixed | 0.610 (0.021) | 0.390 (0.021) | 0.260 (0.029) | 0.479 (0.061) |
| disjoint | 188.77 | RandomForest | 0.418 (0.021) | 0.582 (0.021) | 0.111 (0.017) | -0.052 (0.054) |
| disjoint | 188.77 | SE OOB-selected | 0.676 (0.023) | 0.324 (0.023) | 0.339 (0.032) | 0.640 (0.029) |
| disjoint | 189.05 | DecisionTree | 0.457 (0.044) | 0.543 (0.044) | 0.180 (0.031) | 0.093 (0.109) |
| disjoint | 189.05 | IRIS_Q42 | 0.611 (0.019) | 0.389 (0.019) | 0.260 (0.023) | 0.482 (0.054) |
| disjoint | 189.05 | QRF test-selected | 0.675 (0.017) | 0.325 (0.017) | 0.331 (0.015) | 0.666 (0.015) |
| disjoint | 189.05 | QRF(q=0.40) fixed | 0.675 (0.024) | 0.325 (0.024) | 0.333 (0.034) | 0.638 (0.035) |
| disjoint | 189.05 | QRF(q=0.41) fixed | 0.664 (0.022) | 0.336 (0.022) | 0.318 (0.031) | 0.626 (0.044) |
| disjoint | 189.05 | QRF(q=0.45) fixed | 0.615 (0.021) | 0.385 (0.021) | 0.259 (0.029) | 0.490 (0.060) |
| disjoint | 189.05 | RandomForest | 0.419 (0.021) | 0.581 (0.021) | 0.110 (0.017) | -0.052 (0.053) |
| disjoint | 189.05 | SE OOB-selected | 0.679 (0.024) | 0.321 (0.024) | 0.338 (0.031) | 0.644 (0.029) |
| disjoint | 189.09 | DecisionTree | 0.456 (0.044) | 0.544 (0.044) | 0.180 (0.031) | 0.092 (0.109) |
| disjoint | 189.09 | IRIS_Q42 | 0.611 (0.019) | 0.389 (0.019) | 0.260 (0.023) | 0.481 (0.054) |
| disjoint | 189.09 | QRF test-selected | 0.675 (0.017) | 0.325 (0.017) | 0.333 (0.016) | 0.666 (0.016) |
| disjoint | 189.09 | QRF(q=0.40) fixed | 0.674 (0.024) | 0.326 (0.024) | 0.333 (0.033) | 0.638 (0.035) |
| disjoint | 189.09 | QRF(q=0.41) fixed | 0.663 (0.022) | 0.337 (0.022) | 0.319 (0.031) | 0.626 (0.044) |
| disjoint | 189.09 | QRF(q=0.45) fixed | 0.615 (0.021) | 0.385 (0.021) | 0.260 (0.029) | 0.489 (0.060) |
| disjoint | 189.09 | RandomForest | 0.419 (0.021) | 0.581 (0.021) | 0.110 (0.017) | -0.052 (0.053) |
| disjoint | 189.09 | SE OOB-selected | 0.679 (0.024) | 0.321 (0.024) | 0.338 (0.031) | 0.643 (0.029) |
| disjoint | 194.10 | DecisionTree | 0.473 (0.038) | 0.527 (0.038) | 0.179 (0.028) | 0.126 (0.093) |
| disjoint | 194.10 | IRIS_Q42 | 0.623 (0.019) | 0.378 (0.019) | 0.257 (0.023) | 0.502 (0.052) |
| disjoint | 194.10 | QRF test-selected | 0.682 (0.015) | 0.318 (0.015) | 0.324 (0.018) | 0.674 (0.017) |
| disjoint | 194.10 | QRF(q=0.40) fixed | 0.684 (0.024) | 0.316 (0.024) | 0.330 (0.035) | 0.648 (0.036) |
| disjoint | 194.10 | QRF(q=0.41) fixed | 0.673 (0.022) | 0.327 (0.022) | 0.315 (0.033) | 0.637 (0.039) |
| disjoint | 194.10 | QRF(q=0.45) fixed | 0.626 (0.022) | 0.374 (0.022) | 0.257 (0.028) | 0.509 (0.062) |
| disjoint | 194.10 | RandomForest | 0.438 (0.018) | 0.562 (0.018) | 0.113 (0.015) | -0.012 (0.046) |
| disjoint | 194.10 | SE OOB-selected | 0.683 (0.022) | 0.317 (0.022) | 0.326 (0.031) | 0.651 (0.031) |
| disjoint | train-sample P24.2 | DecisionTree | 0.462 (0.041) | 0.538 (0.041) | 0.181 (0.028) | 0.104 (0.097) |
| disjoint | train-sample P24.2 | IRIS_Q42 | 0.615 (0.020) | 0.385 (0.020) | 0.262 (0.026) | 0.492 (0.050) |
| disjoint | train-sample P24.2 | QRF test-selected | 0.676 (0.020) | 0.324 (0.020) | 0.330 (0.018) | 0.667 (0.018) |
| disjoint | train-sample P24.2 | QRF(q=0.40) fixed | 0.676 (0.020) | 0.324 (0.020) | 0.333 (0.037) | 0.644 (0.032) |
| disjoint | train-sample P24.2 | QRF(q=0.41) fixed | 0.665 (0.020) | 0.335 (0.020) | 0.317 (0.035) | 0.629 (0.033) |
| disjoint | train-sample P24.2 | QRF(q=0.45) fixed | 0.617 (0.018) | 0.383 (0.018) | 0.260 (0.032) | 0.494 (0.051) |
| disjoint | train-sample P24.2 | RandomForest | 0.428 (0.022) | 0.572 (0.022) | 0.114 (0.018) | -0.030 (0.051) |
| disjoint | train-sample P24.2 | SE OOB-selected | 0.679 (0.023) | 0.321 (0.023) | 0.333 (0.038) | 0.643 (0.035) |
| paper | 188.77 | DecisionTree | 0.475 (0.045) | 0.525 (0.045) | 0.170 (0.031) | 0.119 (0.112) |
| paper | 188.77 | IRIS_Q42 | 0.613 (0.018) | 0.387 (0.018) | 0.261 (0.034) | 0.488 (0.054) |
| paper | 188.77 | QRF test-selected | 0.710 (0.019) | 0.290 (0.019) | 0.300 (0.020) | 0.699 (0.019) |
| paper | 188.77 | QRF(q=0.40) fixed | 0.707 (0.030) | 0.293 (0.030) | 0.298 (0.033) | 0.669 (0.041) |
| paper | 188.77 | QRF(q=0.41) fixed | 0.696 (0.031) | 0.304 (0.031) | 0.283 (0.032) | 0.655 (0.054) |
| paper | 188.77 | QRF(q=0.45) fixed | 0.650 (0.032) | 0.350 (0.032) | 0.230 (0.028) | 0.530 (0.073) |
| paper | 188.77 | RandomForest | 0.458 (0.032) | 0.542 (0.032) | 0.098 (0.020) | 0.014 (0.074) |
| paper | 188.77 | SE OOB-selected | 0.708 (0.026) | 0.292 (0.026) | 0.299 (0.026) | 0.677 (0.027) |
| paper | 189.05 | DecisionTree | 0.476 (0.043) | 0.524 (0.043) | 0.168 (0.032) | 0.120 (0.109) |
| paper | 189.05 | IRIS_Q42 | 0.614 (0.018) | 0.387 (0.018) | 0.257 (0.034) | 0.484 (0.053) |
| paper | 189.05 | QRF test-selected | 0.711 (0.020) | 0.289 (0.020) | 0.296 (0.021) | 0.703 (0.021) |
| paper | 189.05 | QRF(q=0.40) fixed | 0.709 (0.030) | 0.291 (0.030) | 0.297 (0.033) | 0.673 (0.040) |
| paper | 189.05 | QRF(q=0.41) fixed | 0.699 (0.030) | 0.301 (0.030) | 0.280 (0.032) | 0.658 (0.053) |
| paper | 189.05 | QRF(q=0.45) fixed | 0.653 (0.032) | 0.347 (0.032) | 0.229 (0.028) | 0.535 (0.072) |
| paper | 189.05 | RandomForest | 0.460 (0.032) | 0.540 (0.032) | 0.096 (0.021) | 0.015 (0.074) |
| paper | 189.05 | SE OOB-selected | 0.711 (0.027) | 0.289 (0.027) | 0.296 (0.028) | 0.680 (0.030) |
| paper | 189.09 | DecisionTree | 0.476 (0.043) | 0.524 (0.043) | 0.167 (0.032) | 0.119 (0.109) |
| paper | 189.09 | IRIS_Q42 | 0.613 (0.018) | 0.387 (0.018) | 0.257 (0.033) | 0.483 (0.052) |
| paper | 189.09 | QRF test-selected | 0.710 (0.021) | 0.290 (0.021) | 0.295 (0.020) | 0.703 (0.021) |
| paper | 189.09 | QRF(q=0.40) fixed | 0.709 (0.030) | 0.291 (0.030) | 0.296 (0.033) | 0.673 (0.040) |
| paper | 189.09 | QRF(q=0.41) fixed | 0.698 (0.030) | 0.302 (0.030) | 0.281 (0.033) | 0.658 (0.053) |
| paper | 189.09 | QRF(q=0.45) fixed | 0.653 (0.032) | 0.347 (0.032) | 0.229 (0.028) | 0.534 (0.072) |
| paper | 189.09 | RandomForest | 0.459 (0.033) | 0.541 (0.033) | 0.095 (0.021) | 0.014 (0.074) |
| paper | 189.09 | SE OOB-selected | 0.711 (0.027) | 0.289 (0.027) | 0.297 (0.028) | 0.679 (0.030) |
| paper | 194.10 | DecisionTree | 0.493 (0.045) | 0.507 (0.045) | 0.173 (0.031) | 0.159 (0.110) |
| paper | 194.10 | IRIS_Q42 | 0.625 (0.016) | 0.375 (0.016) | 0.252 (0.031) | 0.502 (0.047) |
| paper | 194.10 | QRF test-selected | 0.715 (0.018) | 0.285 (0.018) | 0.289 (0.018) | 0.708 (0.017) |
| paper | 194.10 | QRF(q=0.40) fixed | 0.721 (0.028) | 0.280 (0.028) | 0.302 (0.032) | 0.678 (0.034) |
| paper | 194.10 | QRF(q=0.41) fixed | 0.710 (0.030) | 0.290 (0.030) | 0.287 (0.033) | 0.671 (0.047) |
| paper | 194.10 | QRF(q=0.45) fixed | 0.665 (0.033) | 0.335 (0.033) | 0.233 (0.028) | 0.563 (0.077) |
| paper | 194.10 | RandomForest | 0.477 (0.033) | 0.523 (0.033) | 0.101 (0.019) | 0.056 (0.074) |
| paper | 194.10 | SE OOB-selected | 0.715 (0.026) | 0.285 (0.026) | 0.292 (0.026) | 0.686 (0.033) |
| paper | train-sample P24.2 | DecisionTree | 0.478 (0.045) | 0.522 (0.045) | 0.170 (0.031) | 0.126 (0.110) |
| paper | train-sample P24.2 | IRIS_Q42 | 0.614 (0.019) | 0.387 (0.019) | 0.262 (0.031) | 0.489 (0.053) |
| paper | train-sample P24.2 | QRF test-selected | 0.709 (0.024) | 0.291 (0.024) | 0.296 (0.020) | 0.701 (0.022) |
| paper | train-sample P24.2 | QRF(q=0.40) fixed | 0.708 (0.030) | 0.292 (0.030) | 0.297 (0.032) | 0.674 (0.043) |
| paper | train-sample P24.2 | QRF(q=0.41) fixed | 0.695 (0.029) | 0.305 (0.029) | 0.282 (0.029) | 0.657 (0.050) |
| paper | train-sample P24.2 | QRF(q=0.45) fixed | 0.651 (0.029) | 0.349 (0.029) | 0.232 (0.026) | 0.534 (0.066) |
| paper | train-sample P24.2 | RandomForest | 0.459 (0.035) | 0.541 (0.035) | 0.099 (0.020) | 0.017 (0.077) |
| paper | train-sample P24.2 | SE OOB-selected | 0.706 (0.028) | 0.294 (0.028) | 0.295 (0.029) | 0.677 (0.036) |

### SE choice (OOB) and test-selected quantile across splits (value: count)

| protocol   | threshold                                      | se_choice_mode   | se_choice_values                                                                                                 | q_test_values                                                                     |
|:-----------|:-----------------------------------------------|:-----------------|:-----------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|
| disjoint   | 188.77 (full-sample P24.03, published Table 3) | QRF(0.40)        | {'QRF(0.37)': 1, 'QRF(0.38)': 4, 'QRF(0.39)': 7, 'QRF(0.40)': 13, 'QRF(0.41)': 1, 'QRF(0.42)': 4}                | {0.35: 1, 0.37: 1, 0.38: 4, 0.39: 6, 0.4: 10, 0.41: 2, 0.42: 4, 0.43: 1, 0.44: 1} |
| disjoint   | 189.05 (IRIS recon., official ~320 Bs)         | QRF(0.40)        | {'QRF(0.37)': 1, 'QRF(0.38)': 4, 'QRF(0.39)': 8, 'QRF(0.40)': 12, 'QRF(0.41)': 1, 'QRF(0.42)': 4}                | {0.36: 1, 0.37: 1, 0.38: 4, 0.39: 6, 0.4: 8, 0.41: 3, 0.42: 5, 0.43: 1, 0.44: 1}  |
| disjoint   | 189.09 (full-sample P24.2)                     | QRF(0.40)        | {'QRF(0.37)': 1, 'QRF(0.38)': 5, 'QRF(0.39)': 7, 'QRF(0.40)': 12, 'QRF(0.41)': 1, 'QRF(0.42)': 4}                | {0.36: 1, 0.37: 1, 0.38: 4, 0.39: 5, 0.4: 10, 0.41: 3, 0.42: 5, 0.44: 1}          |
| disjoint   | 194.10 (IRIS recon., official ~328 Bs)         | QRF(0.40)        | {'QRF(0.38)': 4, 'QRF(0.39)': 3, 'QRF(0.40)': 13, 'QRF(0.41)': 5, 'QRF(0.42)': 4, 'QRF(0.43)': 1}                | {0.36: 1, 0.37: 1, 0.38: 1, 0.39: 6, 0.4: 10, 0.41: 4, 0.42: 4, 0.43: 2, 0.44: 1} |
| disjoint   | train-sample P24.2                             | QRF(0.40)        | {'QRF(0.38)': 2, 'QRF(0.39)': 7, 'QRF(0.40)': 16, 'QRF(0.41)': 3, 'QRF(0.42)': 1, 'QRF(0.43)': 1}                | {0.36: 1, 0.37: 2, 0.38: 1, 0.39: 6, 0.4: 12, 0.41: 1, 0.42: 6, 0.44: 1}          |
| paper      | 188.77 (full-sample P24.03, published Table 3) | QRF(0.39)        | {'QRF(0.37)': 1, 'QRF(0.38)': 3, 'QRF(0.39)': 8, 'QRF(0.40)': 8, 'QRF(0.41)': 7, 'QRF(0.42)': 2, 'QRF(0.43)': 1} | {0.36: 1, 0.38: 5, 0.39: 6, 0.4: 6, 0.41: 8, 0.42: 2, 0.43: 2}                    |
| paper      | 189.05 (IRIS recon., official ~320 Bs)         | QRF(0.39)        | {'QRF(0.37)': 1, 'QRF(0.38)': 3, 'QRF(0.39)': 8, 'QRF(0.40)': 8, 'QRF(0.41)': 6, 'QRF(0.42)': 3, 'QRF(0.43)': 1} | {0.36: 1, 0.37: 1, 0.38: 5, 0.39: 5, 0.4: 5, 0.41: 9, 0.42: 1, 0.43: 2, 0.44: 1}  |
| paper      | 189.09 (full-sample P24.2)                     | QRF(0.39)        | {'QRF(0.36)': 1, 'QRF(0.38)': 3, 'QRF(0.39)': 8, 'QRF(0.40)': 8, 'QRF(0.41)': 6, 'QRF(0.42)': 3, 'QRF(0.43)': 1} | {0.37: 2, 0.38: 5, 0.39: 5, 0.4: 5, 0.41: 9, 0.42: 1, 0.43: 2, 0.44: 1}           |
| paper      | 194.10 (IRIS recon., official ~328 Bs)         | QRF(0.40)        | {'QRF(0.38)': 2, 'QRF(0.39)': 6, 'QRF(0.40)': 7, 'QRF(0.41)': 7, 'QRF(0.42)': 6, 'QRF(0.43)': 1, 'QRF(0.44)': 1} | {0.37: 1, 0.38: 3, 0.39: 5, 0.4: 4, 0.41: 8, 0.42: 5, 0.43: 2, 0.44: 1, 0.45: 1}  |
| paper      | train-sample P24.2                             | QRF(0.40)        | {'QRF(0.38)': 4, 'QRF(0.39)': 7, 'QRF(0.40)': 9, 'QRF(0.41)': 4, 'QRF(0.42)': 5, 'QRF(0.43)': 1}                 | {0.37: 1, 0.38: 6, 0.39: 6, 0.4: 7, 0.41: 5, 0.42: 4, 0.43: 1}                    |
