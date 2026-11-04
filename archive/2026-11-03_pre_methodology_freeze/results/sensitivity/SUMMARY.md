# Sensitivity analysis — Bolivia EH 2005

Mean of 1000 bootstrap re-draws of the test sample, 95% percentile CI in brackets.
Seed 42. `paper` = overlapping N/2 bootstrap split; `disjoint` = untouched 50/50 test set.

## Protocol: paper

### Threshold 189.09 (full-sample P24.2) — test poverty rate 23.25%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.707 [0.659, 0.755] | 0.512 [0.468, 0.557] | 0.203 [0.162, 0.251] | 0.255 [0.124, 0.369] |
| RandomForest | 0.812 [0.768, 0.856] | 0.519 [0.477, 0.565] | 0.112 [0.082, 0.143] | 0.121 [-0.054, 0.265] |
| IRIS_Q42 | 0.662 [0.616, 0.709] | 0.367 [0.324, 0.411] | 0.324 [0.265, 0.387] | 0.611 [0.538, 0.665] |
| QRF(q=0.40) fixed | 0.695 [0.655, 0.736] | 0.295 [0.255, 0.338] | 0.310 [0.255, 0.369] | 0.665 [0.583, 0.719] |
| QRF(q=0.45) fixed | 0.731 [0.690, 0.773] | 0.337 [0.296, 0.382] | 0.244 [0.197, 0.292] | 0.627 [0.554, 0.691] |
| QRF CV-selected (q=0.45) | 0.731 [0.690, 0.773] | 0.337 [0.296, 0.382] | 0.244 [0.197, 0.292] | 0.627 [0.554, 0.691] |
| QRF test-selected (q=0.40) | 0.695 [0.655, 0.736] | 0.295 [0.255, 0.338] | 0.310 [0.255, 0.369] | 0.665 [0.583, 0.719] |

### Threshold 189.05 (IRIS recon., official ~320 Bs) — test poverty rate 23.20%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.707 [0.659, 0.755] | 0.511 [0.468, 0.556] | 0.203 [0.162, 0.251] | 0.258 [0.128, 0.370] |
| RandomForest | 0.812 [0.768, 0.856] | 0.518 [0.476, 0.563] | 0.112 [0.082, 0.143] | 0.125 [-0.046, 0.268] |
| IRIS_Q42 | 0.662 [0.616, 0.709] | 0.365 [0.323, 0.409] | 0.325 [0.265, 0.388] | 0.613 [0.541, 0.665] |
| QRF(q=0.40) fixed | 0.695 [0.655, 0.736] | 0.293 [0.253, 0.336] | 0.310 [0.255, 0.370] | 0.664 [0.581, 0.719] |
| QRF(q=0.45) fixed | 0.731 [0.690, 0.773] | 0.336 [0.295, 0.379] | 0.245 [0.197, 0.292] | 0.629 [0.558, 0.692] |
| QRF CV-selected (q=0.45) | 0.731 [0.690, 0.773] | 0.336 [0.295, 0.379] | 0.245 [0.197, 0.292] | 0.629 [0.558, 0.692] |
| QRF test-selected (q=0.40) | 0.695 [0.655, 0.736] | 0.293 [0.253, 0.336] | 0.310 [0.255, 0.370] | 0.664 [0.581, 0.719] |

### Threshold 194.10 (IRIS recon., official ~328 Bs) — test poverty rate 24.62%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.719 [0.670, 0.765] | 0.505 [0.464, 0.548] | 0.194 [0.156, 0.239] | 0.263 [0.135, 0.369] |
| RandomForest | 0.820 [0.776, 0.862] | 0.518 [0.472, 0.560] | 0.106 [0.079, 0.135] | 0.117 [-0.041, 0.253] |
| IRIS_Q42 | 0.695 [0.652, 0.738] | 0.352 [0.311, 0.395] | 0.285 [0.233, 0.342] | 0.620 [0.546, 0.677] |
| QRF(q=0.40) fixed | 0.709 [0.671, 0.748] | 0.276 [0.238, 0.317] | 0.297 [0.244, 0.352] | 0.678 [0.599, 0.732] |
| QRF(q=0.45) fixed | 0.739 [0.700, 0.780] | 0.334 [0.291, 0.377] | 0.235 [0.190, 0.282] | 0.628 [0.555, 0.692] |
| QRF CV-selected (q=0.45) | 0.739 [0.700, 0.780] | 0.334 [0.291, 0.377] | 0.235 [0.190, 0.282] | 0.628 [0.555, 0.692] |
| QRF test-selected (q=0.40) | 0.709 [0.671, 0.748] | 0.276 [0.238, 0.317] | 0.297 [0.244, 0.352] | 0.678 [0.599, 0.732] |

### Threshold train-sample P24.2 — test poverty rate 22.22%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.701 [0.647, 0.753] | 0.560 [0.517, 0.602] | 0.188 [0.146, 0.235] | 0.104 [-0.052, 0.245] |
| RandomForest | 0.803 [0.758, 0.849] | 0.534 [0.490, 0.578] | 0.115 [0.084, 0.147] | 0.076 [-0.095, 0.231] |
| IRIS_Q42 | 0.656 [0.613, 0.703] | 0.375 [0.331, 0.419] | 0.328 [0.267, 0.394] | 0.601 [0.533, 0.658] |
| QRF(q=0.40) fixed | 0.683 [0.641, 0.725] | 0.304 [0.263, 0.348] | 0.324 [0.265, 0.389] | 0.650 [0.561, 0.707] |
| QRF(q=0.45) fixed | 0.722 [0.681, 0.763] | 0.344 [0.302, 0.388] | 0.253 [0.204, 0.307] | 0.621 [0.548, 0.685] |
| QRF CV-selected (q=0.40) | 0.683 [0.641, 0.725] | 0.304 [0.263, 0.348] | 0.324 [0.265, 0.389] | 0.650 [0.561, 0.707] |
| QRF test-selected (q=0.40) | 0.683 [0.641, 0.725] | 0.304 [0.263, 0.348] | 0.324 [0.265, 0.389] | 0.650 [0.561, 0.707] |

## Protocol: disjoint

### Threshold 189.09 (full-sample P24.2) — test poverty rate 23.25%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.730 [0.675, 0.784] | 0.596 [0.555, 0.637] | 0.150 [0.114, 0.190] | -0.081 [-0.258, 0.073] |
| RandomForest | 0.794 [0.741, 0.840] | 0.579 [0.534, 0.624] | 0.109 [0.080, 0.144] | -0.096 [-0.295, 0.074] |
| IRIS_Q42 | 0.704 [0.657, 0.748] | 0.376 [0.335, 0.422] | 0.263 [0.211, 0.318] | 0.574 [0.495, 0.642] |
| QRF(q=0.40) fixed | 0.652 [0.610, 0.693] | 0.345 [0.303, 0.386] | 0.350 [0.294, 0.412] | 0.622 [0.547, 0.671] |
| QRF(q=0.45) fixed | 0.677 [0.632, 0.722] | 0.404 [0.361, 0.447] | 0.285 [0.234, 0.341] | 0.540 [0.458, 0.616] |
| QRF CV-selected (q=0.40) | 0.652 [0.610, 0.693] | 0.345 [0.303, 0.386] | 0.350 [0.294, 0.412] | 0.622 [0.547, 0.671] |
| QRF test-selected (q=0.40) | 0.652 [0.610, 0.693] | 0.345 [0.303, 0.386] | 0.350 [0.294, 0.412] | 0.622 [0.547, 0.671] |

### Threshold 189.05 (IRIS recon., official ~320 Bs) — test poverty rate 23.20%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.730 [0.675, 0.784] | 0.595 [0.553, 0.636] | 0.150 [0.114, 0.190] | -0.077 [-0.253, 0.076] |
| RandomForest | 0.794 [0.741, 0.840] | 0.578 [0.533, 0.624] | 0.110 [0.080, 0.144] | -0.093 [-0.289, 0.076] |
| IRIS_Q42 | 0.704 [0.657, 0.748] | 0.375 [0.333, 0.420] | 0.263 [0.211, 0.319] | 0.576 [0.499, 0.644] |
| QRF(q=0.40) fixed | 0.652 [0.610, 0.693] | 0.343 [0.301, 0.386] | 0.351 [0.294, 0.413] | 0.622 [0.544, 0.672] |
| QRF(q=0.45) fixed | 0.677 [0.632, 0.722] | 0.402 [0.359, 0.446] | 0.285 [0.235, 0.341] | 0.543 [0.461, 0.617] |
| QRF CV-selected (q=0.40) | 0.652 [0.610, 0.693] | 0.343 [0.301, 0.386] | 0.351 [0.294, 0.413] | 0.622 [0.544, 0.672] |
| QRF test-selected (q=0.40) | 0.652 [0.610, 0.693] | 0.343 [0.301, 0.386] | 0.351 [0.294, 0.413] | 0.622 [0.544, 0.672] |

### Threshold 194.10 (IRIS recon., official ~328 Bs) — test poverty rate 24.23%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.749 [0.696, 0.800] | 0.578 [0.536, 0.618] | 0.142 [0.108, 0.179] | -0.030 [-0.195, 0.120] |
| RandomForest | 0.805 [0.756, 0.851] | 0.559 [0.516, 0.605] | 0.107 [0.079, 0.138] | -0.026 [-0.210, 0.129] |
| IRIS_Q42 | 0.716 [0.672, 0.758] | 0.369 [0.330, 0.413] | 0.250 [0.204, 0.303] | 0.579 [0.506, 0.647] |
| QRF(q=0.40) fixed | 0.677 [0.637, 0.717] | 0.331 [0.291, 0.369] | 0.320 [0.267, 0.378] | 0.647 [0.586, 0.694] |
| QRF(q=0.45) fixed | 0.696 [0.652, 0.739] | 0.389 [0.347, 0.429] | 0.267 [0.219, 0.319] | 0.555 [0.482, 0.626] |
| QRF CV-selected (q=0.40) | 0.677 [0.637, 0.717] | 0.331 [0.291, 0.369] | 0.320 [0.267, 0.378] | 0.647 [0.586, 0.694] |
| QRF test-selected (q=0.40) | 0.677 [0.637, 0.717] | 0.331 [0.291, 0.369] | 0.320 [0.267, 0.378] | 0.647 [0.586, 0.694] |

### Threshold train-sample P24.2 — test poverty rate 22.52%

| Model | PA | UC | LE | BPAC |
|---|---|---|---|---|
| DecisionTree | 0.722 [0.665, 0.775] | 0.587 [0.543, 0.628] | 0.159 [0.121, 0.201] | -0.032 [-0.202, 0.120] |
| RandomForest | 0.799 [0.743, 0.848] | 0.587 [0.543, 0.635] | 0.104 [0.075, 0.137] | -0.141 [-0.350, 0.038] |
| IRIS_Q42 | 0.693 [0.646, 0.739] | 0.389 [0.348, 0.433] | 0.271 [0.219, 0.327] | 0.559 [0.477, 0.629] |
| QRF(q=0.40) fixed | 0.645 [0.600, 0.687] | 0.356 [0.313, 0.398] | 0.355 [0.297, 0.419] | 0.614 [0.541, 0.664] |
| QRF(q=0.45) fixed | 0.673 [0.627, 0.720] | 0.410 [0.365, 0.454] | 0.288 [0.235, 0.346] | 0.531 [0.446, 0.609] |
| QRF CV-selected (q=0.40) | 0.645 [0.600, 0.687] | 0.356 [0.313, 0.398] | 0.355 [0.297, 0.419] | 0.614 [0.541, 0.664] |
| QRF test-selected (q=0.40) | 0.645 [0.600, 0.687] | 0.356 [0.313, 0.398] | 0.355 [0.297, 0.419] | 0.614 [0.541, 0.664] |

## Step 2 — paired difference QRF(40) − QRF(45)

| Protocol | Threshold | Metric | Diff | 95% CI | CI excludes 0 |
|---|---|---|---|---|---|
| paper | 189.09 (full-sample P24.2) | PA | -0.0358 | [-0.0549, -0.0175] | yes |
| paper | 189.09 (full-sample P24.2) | UC | -0.0422 | [-0.0613, -0.0258] | yes |
| paper | 189.09 (full-sample P24.2) | LE | +0.0653 | [+0.0414, +0.0907] | yes |
| paper | 189.09 (full-sample P24.2) | BPAC | +0.0376 | [-0.0869, +0.1087] | no |
| paper | 189.05 (IRIS recon., official ~320 Bs) | PA | -0.0358 | [-0.0549, -0.0175] | yes |
| paper | 189.05 (IRIS recon., official ~320 Bs) | UC | -0.0423 | [-0.0613, -0.0258] | yes |
| paper | 189.05 (IRIS recon., official ~320 Bs) | LE | +0.0655 | [+0.0414, +0.0907] | yes |
| paper | 189.05 (IRIS recon., official ~320 Bs) | BPAC | +0.0347 | [-0.0896, +0.1079] | no |
| paper | 194.10 (IRIS recon., official ~328 Bs) | PA | -0.0300 | [-0.0473, -0.0137] | yes |
| paper | 194.10 (IRIS recon., official ~328 Bs) | UC | -0.0576 | [-0.0802, -0.0379] | yes |
| paper | 194.10 (IRIS recon., official ~328 Bs) | LE | +0.0618 | [+0.0410, +0.0854] | yes |
| paper | 194.10 (IRIS recon., official ~328 Bs) | BPAC | +0.0497 | [-0.0760, +0.1292] | no |
| paper | train-sample P24.2 | PA | -0.0394 | [-0.0581, -0.0200] | yes |
| paper | train-sample P24.2 | UC | -0.0397 | [-0.0591, -0.0226] | yes |
| paper | train-sample P24.2 | LE | +0.0710 | [+0.0445, +0.0993] | yes |
| paper | train-sample P24.2 | BPAC | +0.0298 | [-0.1026, +0.1085] | no |
| disjoint | 189.09 (full-sample P24.2) | PA | -0.0248 | [-0.0428, -0.0072] | yes |
| disjoint | 189.09 (full-sample P24.2) | UC | -0.0591 | [-0.0813, -0.0402] | yes |
| disjoint | 189.09 (full-sample P24.2) | LE | +0.0651 | [+0.0430, +0.0917] | yes |
| disjoint | 189.09 (full-sample P24.2) | BPAC | +0.0819 | [-0.0523, +0.1526] | no |
| disjoint | 189.05 (IRIS recon., official ~320 Bs) | PA | -0.0248 | [-0.0428, -0.0072] | yes |
| disjoint | 189.05 (IRIS recon., official ~320 Bs) | UC | -0.0592 | [-0.0813, -0.0402] | yes |
| disjoint | 189.05 (IRIS recon., official ~320 Bs) | LE | +0.0652 | [+0.0432, +0.0917] | yes |
| disjoint | 189.05 (IRIS recon., official ~320 Bs) | BPAC | +0.0795 | [-0.0556, +0.1511] | no |
| disjoint | 194.10 (IRIS recon., official ~328 Bs) | PA | -0.0187 | [-0.0360, -0.0026] | yes |
| disjoint | 194.10 (IRIS recon., official ~328 Bs) | UC | -0.0587 | [-0.0808, -0.0385] | yes |
| disjoint | 194.10 (IRIS recon., official ~328 Bs) | LE | +0.0523 | [+0.0329, +0.0731] | yes |
| disjoint | 194.10 (IRIS recon., official ~328 Bs) | BPAC | +0.0915 | [-0.0167, +0.1470] | no |
| disjoint | train-sample P24.2 | PA | -0.0274 | [-0.0461, -0.0099] | yes |
| disjoint | train-sample P24.2 | UC | -0.0545 | [-0.0777, -0.0346] | yes |
| disjoint | train-sample P24.2 | LE | +0.0672 | [+0.0462, +0.0918] | yes |
| disjoint | train-sample P24.2 | BPAC | +0.0835 | [-0.0469, +0.1488] | no |

## Step 3 — paired difference vs 189.09 Bs (same model, same test resamples)

| Protocol | Model | Change | Metric | Diff | 95% CI | CI excludes 0 |
|---|---|---|---|---|---|---|
| paper | DecisionTree | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| paper | DecisionTree | 189.05 − 189.09 | UC | -0.0010 | [-0.0032, +0.0000] | no |
| paper | DecisionTree | 189.05 − 189.09 | LE | +0.0004 | [+0.0000, +0.0014] | no |
| paper | DecisionTree | 189.05 − 189.09 | BPAC | +0.0031 | [+0.0000, +0.0095] | no |
| paper | RandomForest | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| paper | RandomForest | 189.05 − 189.09 | UC | -0.0010 | [-0.0032, +0.0000] | no |
| paper | RandomForest | 189.05 − 189.09 | LE | +0.0002 | [+0.0000, +0.0008] | no |
| paper | RandomForest | 189.05 − 189.09 | BPAC | +0.0036 | [+0.0000, +0.0112] | no |
| paper | IRIS_Q42 | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| paper | IRIS_Q42 | 189.05 − 189.09 | UC | -0.0013 | [-0.0041, +0.0000] | no |
| paper | IRIS_Q42 | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0022] | no |
| paper | IRIS_Q42 | 189.05 − 189.09 | BPAC | +0.0018 | [-0.0025, +0.0068] | no |
| paper | QRF(q=0.40) fixed | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| paper | QRF(q=0.40) fixed | 189.05 − 189.09 | UC | -0.0015 | [-0.0046, +0.0000] | no |
| paper | QRF(q=0.40) fixed | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0021] | no |
| paper | QRF(q=0.40) fixed | 189.05 − 189.09 | BPAC | -0.0006 | [-0.0061, +0.0046] | no |
| paper | QRF(q=0.45) fixed | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| paper | QRF(q=0.45) fixed | 189.05 − 189.09 | UC | -0.0014 | [-0.0043, +0.0000] | no |
| paper | QRF(q=0.45) fixed | 189.05 − 189.09 | LE | +0.0005 | [+0.0000, +0.0017] | no |
| paper | QRF(q=0.45) fixed | 189.05 − 189.09 | BPAC | +0.0023 | [+0.0000, +0.0071] | no |
| paper | QRF CV-selected | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| paper | QRF CV-selected | 189.05 − 189.09 | UC | -0.0014 | [-0.0043, +0.0000] | no |
| paper | QRF CV-selected | 189.05 − 189.09 | LE | +0.0005 | [+0.0000, +0.0017] | no |
| paper | QRF CV-selected | 189.05 − 189.09 | BPAC | +0.0023 | [+0.0000, +0.0071] | no |
| paper | QRF test-selected | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| paper | QRF test-selected | 189.05 − 189.09 | UC | -0.0015 | [-0.0046, +0.0000] | no |
| paper | QRF test-selected | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0021] | no |
| paper | QRF test-selected | 189.05 − 189.09 | BPAC | -0.0006 | [-0.0061, +0.0046] | no |
| paper | DecisionTree | 194.10 − 189.09 | PA | +0.0123 | [-0.0078, +0.0322] | no |
| paper | DecisionTree | 194.10 − 189.09 | UC | -0.0069 | [-0.0234, +0.0093] | no |
| paper | DecisionTree | 194.10 − 189.09 | LE | -0.0091 | [-0.0279, +0.0082] | no |
| paper | DecisionTree | 194.10 − 189.09 | BPAC | +0.0079 | [-0.0330, +0.0516] | no |
| paper | RandomForest | 194.10 − 189.09 | PA | +0.0084 | [-0.0113, +0.0284] | no |
| paper | RandomForest | 194.10 − 189.09 | UC | -0.0012 | [-0.0167, +0.0144] | no |
| paper | RandomForest | 194.10 − 189.09 | LE | -0.0059 | [-0.0194, +0.0076] | no |
| paper | RandomForest | 194.10 − 189.09 | BPAC | -0.0046 | [-0.0555, +0.0495] | no |
| paper | IRIS_Q42 | 194.10 − 189.09 | PA | +0.0329 | [+0.0122, +0.0546] | yes |
| paper | IRIS_Q42 | 194.10 − 189.09 | UC | -0.0143 | [-0.0301, -0.0009] | yes |
| paper | IRIS_Q42 | 194.10 − 189.09 | LE | -0.0392 | [-0.0689, -0.0126] | yes |
| paper | IRIS_Q42 | 194.10 − 189.09 | BPAC | +0.0092 | [-0.0141, +0.0613] | no |
| paper | QRF(q=0.40) fixed | 194.10 − 189.09 | PA | +0.0141 | [-0.0024, +0.0314] | no |
| paper | QRF(q=0.40) fixed | 194.10 − 189.09 | UC | -0.0185 | [-0.0373, +0.0000] | no |
| paper | QRF(q=0.40) fixed | 194.10 − 189.09 | LE | -0.0126 | [-0.0367, +0.0103] | no |
| paper | QRF(q=0.40) fixed | 194.10 − 189.09 | BPAC | +0.0132 | [-0.0253, +0.0479] | no |
| paper | QRF(q=0.45) fixed | 194.10 − 189.09 | PA | +0.0082 | [-0.0080, +0.0253] | no |
| paper | QRF(q=0.45) fixed | 194.10 − 189.09 | UC | -0.0031 | [-0.0218, +0.0135] | no |
| paper | QRF(q=0.45) fixed | 194.10 − 189.09 | LE | -0.0091 | [-0.0289, +0.0099] | no |
| paper | QRF(q=0.45) fixed | 194.10 − 189.09 | BPAC | +0.0011 | [-0.0263, +0.0296] | no |
| paper | QRF CV-selected | 194.10 − 189.09 | PA | +0.0082 | [-0.0080, +0.0253] | no |
| paper | QRF CV-selected | 194.10 − 189.09 | UC | -0.0031 | [-0.0218, +0.0135] | no |
| paper | QRF CV-selected | 194.10 − 189.09 | LE | -0.0091 | [-0.0289, +0.0099] | no |
| paper | QRF CV-selected | 194.10 − 189.09 | BPAC | +0.0011 | [-0.0263, +0.0296] | no |
| paper | QRF test-selected | 194.10 − 189.09 | PA | +0.0141 | [-0.0024, +0.0314] | no |
| paper | QRF test-selected | 194.10 − 189.09 | UC | -0.0185 | [-0.0373, +0.0000] | no |
| paper | QRF test-selected | 194.10 − 189.09 | LE | -0.0126 | [-0.0367, +0.0103] | no |
| paper | QRF test-selected | 194.10 − 189.09 | BPAC | +0.0132 | [-0.0253, +0.0479] | no |
| paper | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0056 | [-0.0323, +0.0199] | no |
| paper | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0478 | [+0.0264, +0.0708] | yes |
| paper | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | LE | -0.0149 | [-0.0372, +0.0069] | no |
| paper | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.1511 | [-0.2202, -0.0826] | yes |
| paper | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0090 | [-0.0269, +0.0085] | no |
| paper | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0152 | [-0.0028, +0.0328] | no |
| paper | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0029 | [-0.0087, +0.0146] | no |
| paper | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0452 | [-0.1035, +0.0125] | no |
| paper | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0059 | [-0.0243, +0.0098] | no |
| paper | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0085 | [-0.0074, +0.0251] | no |
| paper | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0042 | [-0.0172, +0.0275] | no |
| paper | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0101 | [-0.0365, +0.0173] | no |
| paper | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0124 | [-0.0298, +0.0026] | no |
| paper | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0092 | [-0.0043, +0.0220] | no |
| paper | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0142 | [-0.0062, +0.0380] | no |
| paper | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0145 | [-0.0522, +0.0142] | no |
| paper | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0088 | [-0.0272, +0.0087] | no |
| paper | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0066 | [-0.0078, +0.0212] | no |
| paper | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0085 | [-0.0127, +0.0303] | no |
| paper | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0066 | [-0.0294, +0.0160] | no |
| paper | QRF CV-selected | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0482 | [-0.0696, -0.0276] | yes |
| paper | QRF CV-selected | train-sample P24.2 minus 189.09 − 189.09 | UC | -0.0330 | [-0.0520, -0.0169] | yes |
| paper | QRF CV-selected | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0796 | [+0.0525, +0.1098] | yes |
| paper | QRF CV-selected | train-sample P24.2 minus 189.09 − 189.09 | BPAC | +0.0232 | [-0.1071, +0.1011] | no |
| paper | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0124 | [-0.0298, +0.0026] | no |
| paper | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0092 | [-0.0043, +0.0220] | no |
| paper | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0142 | [-0.0062, +0.0380] | no |
| paper | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0145 | [-0.0522, +0.0142] | no |
| disjoint | DecisionTree | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| disjoint | DecisionTree | 189.05 − 189.09 | UC | -0.0008 | [-0.0027, +0.0000] | no |
| disjoint | DecisionTree | 189.05 − 189.09 | LE | +0.0003 | [+0.0000, +0.0010] | no |
| disjoint | DecisionTree | 189.05 − 189.09 | BPAC | +0.0037 | [+0.0000, +0.0121] | no |
| disjoint | RandomForest | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| disjoint | RandomForest | 189.05 − 189.09 | UC | -0.0009 | [-0.0028, +0.0000] | no |
| disjoint | RandomForest | 189.05 − 189.09 | LE | +0.0002 | [+0.0000, +0.0007] | no |
| disjoint | RandomForest | 189.05 − 189.09 | BPAC | +0.0039 | [+0.0000, +0.0127] | no |
| disjoint | IRIS_Q42 | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| disjoint | IRIS_Q42 | 189.05 − 189.09 | UC | -0.0013 | [-0.0041, +0.0000] | no |
| disjoint | IRIS_Q42 | 189.05 − 189.09 | LE | +0.0005 | [+0.0000, +0.0018] | no |
| disjoint | IRIS_Q42 | 189.05 − 189.09 | BPAC | +0.0023 | [+0.0000, +0.0074] | no |
| disjoint | QRF(q=0.40) fixed | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| disjoint | QRF(q=0.40) fixed | 189.05 − 189.09 | UC | -0.0013 | [-0.0043, +0.0000] | no |
| disjoint | QRF(q=0.40) fixed | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0025] | no |
| disjoint | QRF(q=0.40) fixed | 189.05 − 189.09 | BPAC | -0.0001 | [-0.0058, +0.0064] | no |
| disjoint | QRF(q=0.45) fixed | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| disjoint | QRF(q=0.45) fixed | 189.05 − 189.09 | UC | -0.0012 | [-0.0039, +0.0000] | no |
| disjoint | QRF(q=0.45) fixed | 189.05 − 189.09 | LE | +0.0006 | [+0.0000, +0.0020] | no |
| disjoint | QRF(q=0.45) fixed | 189.05 − 189.09 | BPAC | +0.0023 | [+0.0000, +0.0074] | no |
| disjoint | QRF CV-selected | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| disjoint | QRF CV-selected | 189.05 − 189.09 | UC | -0.0013 | [-0.0043, +0.0000] | no |
| disjoint | QRF CV-selected | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0025] | no |
| disjoint | QRF CV-selected | 189.05 − 189.09 | BPAC | -0.0001 | [-0.0058, +0.0064] | no |
| disjoint | QRF test-selected | 189.05 − 189.09 | PA | +0.0000 | [+0.0000, +0.0000] | no |
| disjoint | QRF test-selected | 189.05 − 189.09 | UC | -0.0013 | [-0.0043, +0.0000] | no |
| disjoint | QRF test-selected | 189.05 − 189.09 | LE | +0.0007 | [+0.0000, +0.0025] | no |
| disjoint | QRF test-selected | 189.05 − 189.09 | BPAC | -0.0001 | [-0.0058, +0.0064] | no |
| disjoint | DecisionTree | 194.10 − 189.09 | PA | +0.0192 | [-0.0030, +0.0424] | no |
| disjoint | DecisionTree | 194.10 − 189.09 | UC | -0.0180 | [-0.0335, -0.0026] | yes |
| disjoint | DecisionTree | 194.10 − 189.09 | LE | -0.0082 | [-0.0226, +0.0064] | no |
| disjoint | DecisionTree | 194.10 − 189.09 | BPAC | +0.0513 | [-0.0068, +0.1101] | no |
| disjoint | RandomForest | 194.10 − 189.09 | PA | +0.0109 | [-0.0121, +0.0350] | no |
| disjoint | RandomForest | 194.10 − 189.09 | UC | -0.0197 | [-0.0382, -0.0038] | yes |
| disjoint | RandomForest | 194.10 − 189.09 | LE | -0.0024 | [-0.0175, +0.0121] | no |
| disjoint | RandomForest | 194.10 − 189.09 | BPAC | +0.0708 | [+0.0101, +0.1373] | yes |
| disjoint | IRIS_Q42 | 194.10 − 189.09 | PA | +0.0124 | [-0.0069, +0.0330] | no |
| disjoint | IRIS_Q42 | 194.10 − 189.09 | UC | -0.0070 | [-0.0177, +0.0042] | no |
| disjoint | IRIS_Q42 | 194.10 − 189.09 | LE | -0.0126 | [-0.0353, +0.0092] | no |
| disjoint | IRIS_Q42 | 194.10 − 189.09 | BPAC | +0.0053 | [-0.0117, +0.0256] | no |
| disjoint | QRF(q=0.40) fixed | 194.10 − 189.09 | PA | +0.0250 | [+0.0097, +0.0415] | yes |
| disjoint | QRF(q=0.40) fixed | 194.10 − 189.09 | UC | -0.0141 | [-0.0284, -0.0006] | yes |
| disjoint | QRF(q=0.40) fixed | 194.10 − 189.09 | LE | -0.0304 | [-0.0515, -0.0093] | yes |
| disjoint | QRF(q=0.40) fixed | 194.10 − 189.09 | BPAC | +0.0244 | [-0.0048, +0.0629] | no |
| disjoint | QRF(q=0.45) fixed | 194.10 − 189.09 | PA | +0.0189 | [+0.0008, +0.0397] | yes |
| disjoint | QRF(q=0.45) fixed | 194.10 − 189.09 | UC | -0.0144 | [-0.0266, -0.0018] | yes |
| disjoint | QRF(q=0.45) fixed | 194.10 − 189.09 | LE | -0.0177 | [-0.0417, +0.0041] | no |
| disjoint | QRF(q=0.45) fixed | 194.10 − 189.09 | BPAC | +0.0149 | [-0.0046, +0.0363] | no |
| disjoint | QRF CV-selected | 194.10 − 189.09 | PA | +0.0250 | [+0.0097, +0.0415] | yes |
| disjoint | QRF CV-selected | 194.10 − 189.09 | UC | -0.0141 | [-0.0284, -0.0006] | yes |
| disjoint | QRF CV-selected | 194.10 − 189.09 | LE | -0.0304 | [-0.0515, -0.0093] | yes |
| disjoint | QRF CV-selected | 194.10 − 189.09 | BPAC | +0.0244 | [-0.0048, +0.0629] | no |
| disjoint | QRF test-selected | 194.10 − 189.09 | PA | +0.0250 | [+0.0097, +0.0415] | yes |
| disjoint | QRF test-selected | 194.10 − 189.09 | UC | -0.0141 | [-0.0284, -0.0006] | yes |
| disjoint | QRF test-selected | 194.10 − 189.09 | LE | -0.0304 | [-0.0515, -0.0093] | yes |
| disjoint | QRF test-selected | 194.10 − 189.09 | BPAC | +0.0244 | [-0.0048, +0.0629] | no |
| disjoint | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0076 | [-0.0187, +0.0000] | no |
| disjoint | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | UC | -0.0087 | [-0.0156, -0.0021] | yes |
| disjoint | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0092 | [+0.0030, +0.0171] | yes |
| disjoint | DecisionTree | train-sample P24.2 minus 189.09 − 189.09 | BPAC | +0.0492 | [+0.0256, +0.0776] | yes |
| disjoint | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | PA | +0.0047 | [-0.0115, +0.0231] | no |
| disjoint | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0082 | [-0.0056, +0.0224] | no |
| disjoint | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | LE | -0.0052 | [-0.0170, +0.0045] | no |
| disjoint | RandomForest | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0444 | [-0.1082, +0.0123] | no |
| disjoint | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0109 | [-0.0274, +0.0045] | no |
| disjoint | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0122 | [-0.0017, +0.0263] | no |
| disjoint | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0086 | [-0.0090, +0.0270] | no |
| disjoint | IRIS_Q42 | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0156 | [-0.0399, +0.0073] | no |
| disjoint | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0070 | [-0.0202, +0.0066] | no |
| disjoint | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0111 | [-0.0025, +0.0253] | no |
| disjoint | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0049 | [-0.0142, +0.0242] | no |
| disjoint | QRF(q=0.40) fixed | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0079 | [-0.0335, +0.0224] | no |
| disjoint | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0045 | [-0.0190, +0.0098] | no |
| disjoint | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0065 | [-0.0070, +0.0212] | no |
| disjoint | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0027 | [-0.0147, +0.0200] | no |
| disjoint | QRF(q=0.45) fixed | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0095 | [-0.0361, +0.0157] | no |
| disjoint | QRF CV-selected | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0070 | [-0.0202, +0.0066] | no |
| disjoint | QRF CV-selected | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0111 | [-0.0025, +0.0253] | no |
| disjoint | QRF CV-selected | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0049 | [-0.0142, +0.0242] | no |
| disjoint | QRF CV-selected | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0079 | [-0.0335, +0.0224] | no |
| disjoint | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | PA | -0.0070 | [-0.0202, +0.0066] | no |
| disjoint | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | UC | +0.0111 | [-0.0025, +0.0253] | no |
| disjoint | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | LE | +0.0049 | [-0.0142, +0.0242] | no |
| disjoint | QRF test-selected | train-sample P24.2 minus 189.09 − 189.09 | BPAC | -0.0079 | [-0.0335, +0.0224] | no |

## Quantile selected (seed 42)

| protocol   | threshold                              |    line |   q_cv_selected |   q_test_selected |
|:-----------|:---------------------------------------|--------:|----------------:|------------------:|
| paper      | 189.09 (full-sample P24.2)             | 189.091 |            0.45 |               0.4 |
| paper      | 189.05 (IRIS recon., official ~320 Bs) | 189.05  |            0.45 |               0.4 |
| paper      | 194.10 (IRIS recon., official ~328 Bs) | 194.1   |            0.45 |               0.4 |
| paper      | train-sample P24.2                     | 185.08  |            0.4  |               0.4 |
| disjoint   | 189.09 (full-sample P24.2)             | 189.091 |            0.4  |               0.4 |
| disjoint   | 189.05 (IRIS recon., official ~320 Bs) | 189.05  |            0.4  |               0.4 |
| disjoint   | 194.10 (IRIS recon., official ~328 Bs) | 194.1   |            0.4  |               0.4 |
| disjoint   | train-sample P24.2                     | 185.52  |            0.4  |               0.4 |

## Repeated splits — mean (SD) of point metrics over 30 random splits per protocol

| Protocol | Threshold | Model | PA | UC | LE | BPAC |
|---|---|---|---|---|---|---|
| disjoint | 189.05 | DecisionTree | 0.718 (0.030) | 0.543 (0.044) | 0.180 (0.031) | 0.130 (0.166) |
| disjoint | 189.05 | IRIS_Q42 | 0.702 (0.017) | 0.389 (0.019) | 0.260 (0.023) | 0.552 (0.039) |
| disjoint | 189.05 | QRF CV-selected | 0.674 (0.018) | 0.334 (0.022) | 0.323 (0.029) | 0.641 (0.031) |
| disjoint | 189.05 | QRF test-selected | 0.674 (0.016) | 0.333 (0.019) | 0.323 (0.023) | 0.649 (0.020) |
| disjoint | 189.05 | QRF(q=0.40) fixed | 0.674 (0.018) | 0.334 (0.022) | 0.323 (0.029) | 0.641 (0.031) |
| disjoint | 189.05 | QRF(q=0.45) fixed | 0.705 (0.019) | 0.396 (0.023) | 0.253 (0.026) | 0.536 (0.047) |
| disjoint | 189.05 | RandomForest | 0.794 (0.022) | 0.581 (0.021) | 0.110 (0.017) | -0.105 (0.107) |
| disjoint | 189.09 | DecisionTree | 0.718 (0.030) | 0.544 (0.044) | 0.180 (0.031) | 0.129 (0.166) |
| disjoint | 189.09 | IRIS_Q42 | 0.702 (0.017) | 0.389 (0.019) | 0.260 (0.023) | 0.551 (0.039) |
| disjoint | 189.09 | QRF CV-selected | 0.674 (0.018) | 0.334 (0.022) | 0.323 (0.029) | 0.641 (0.031) |
| disjoint | 189.09 | QRF test-selected | 0.674 (0.016) | 0.333 (0.019) | 0.323 (0.023) | 0.648 (0.020) |
| disjoint | 189.09 | QRF(q=0.40) fixed | 0.674 (0.018) | 0.334 (0.022) | 0.323 (0.029) | 0.641 (0.031) |
| disjoint | 189.09 | QRF(q=0.45) fixed | 0.705 (0.019) | 0.396 (0.023) | 0.253 (0.026) | 0.535 (0.047) |
| disjoint | 189.09 | RandomForest | 0.793 (0.022) | 0.581 (0.021) | 0.110 (0.017) | -0.105 (0.108) |
| disjoint | 194.10 | DecisionTree | 0.726 (0.028) | 0.527 (0.038) | 0.179 (0.028) | 0.182 (0.131) |
| disjoint | 194.10 | IRIS_Q42 | 0.708 (0.016) | 0.378 (0.019) | 0.257 (0.023) | 0.569 (0.037) |
| disjoint | 194.10 | QRF CV-selected | 0.679 (0.020) | 0.322 (0.021) | 0.321 (0.032) | 0.645 (0.033) |
| disjoint | 194.10 | QRF test-selected | 0.682 (0.017) | 0.325 (0.019) | 0.315 (0.025) | 0.653 (0.022) |
| disjoint | 194.10 | QRF(q=0.40) fixed | 0.679 (0.020) | 0.322 (0.021) | 0.321 (0.032) | 0.645 (0.033) |
| disjoint | 194.10 | QRF(q=0.45) fixed | 0.712 (0.020) | 0.382 (0.021) | 0.251 (0.026) | 0.559 (0.043) |
| disjoint | 194.10 | RandomForest | 0.796 (0.019) | 0.562 (0.018) | 0.113 (0.015) | -0.026 (0.085) |
| disjoint | train-sample P24.2 | DecisionTree | 0.719 (0.030) | 0.538 (0.041) | 0.181 (0.028) | 0.151 (0.138) |
| disjoint | train-sample P24.2 | IRIS_Q42 | 0.702 (0.022) | 0.385 (0.020) | 0.262 (0.026) | 0.560 (0.036) |
| disjoint | train-sample P24.2 | QRF CV-selected | 0.675 (0.024) | 0.332 (0.021) | 0.322 (0.036) | 0.641 (0.033) |
| disjoint | train-sample P24.2 | QRF test-selected | 0.674 (0.020) | 0.331 (0.020) | 0.324 (0.026) | 0.648 (0.023) |
| disjoint | train-sample P24.2 | QRF(q=0.40) fixed | 0.674 (0.022) | 0.331 (0.019) | 0.325 (0.032) | 0.644 (0.028) |
| disjoint | train-sample P24.2 | QRF(q=0.45) fixed | 0.707 (0.023) | 0.393 (0.019) | 0.253 (0.026) | 0.541 (0.035) |
| disjoint | train-sample P24.2 | RandomForest | 0.791 (0.027) | 0.572 (0.022) | 0.114 (0.018) | -0.061 (0.097) |
| paper | 189.05 | DecisionTree | 0.741 (0.029) | 0.524 (0.043) | 0.168 (0.032) | 0.171 (0.157) |
| paper | 189.05 | IRIS_Q42 | 0.706 (0.027) | 0.387 (0.018) | 0.257 (0.034) | 0.554 (0.038) |
| paper | 189.05 | QRF CV-selected | 0.713 (0.022) | 0.292 (0.030) | 0.285 (0.030) | 0.675 (0.036) |
| paper | 189.05 | QRF test-selected | 0.715 (0.022) | 0.294 (0.026) | 0.282 (0.029) | 0.680 (0.029) |
| paper | 189.05 | QRF(q=0.40) fixed | 0.713 (0.022) | 0.292 (0.030) | 0.285 (0.030) | 0.675 (0.036) |
| paper | 189.05 | QRF(q=0.45) fixed | 0.749 (0.027) | 0.350 (0.027) | 0.218 (0.031) | 0.595 (0.048) |
| paper | 189.05 | RandomForest | 0.829 (0.029) | 0.540 (0.032) | 0.096 (0.021) | 0.017 (0.128) |
| paper | 189.09 | DecisionTree | 0.742 (0.029) | 0.524 (0.043) | 0.167 (0.032) | 0.169 (0.158) |
| paper | 189.09 | IRIS_Q42 | 0.705 (0.026) | 0.387 (0.018) | 0.257 (0.033) | 0.553 (0.037) |
| paper | 189.09 | QRF CV-selected | 0.713 (0.022) | 0.293 (0.030) | 0.285 (0.030) | 0.675 (0.036) |
| paper | 189.09 | QRF test-selected | 0.715 (0.022) | 0.294 (0.026) | 0.282 (0.029) | 0.680 (0.029) |
| paper | 189.09 | QRF(q=0.40) fixed | 0.713 (0.022) | 0.293 (0.030) | 0.285 (0.030) | 0.675 (0.036) |
| paper | 189.09 | QRF(q=0.45) fixed | 0.749 (0.027) | 0.350 (0.027) | 0.218 (0.031) | 0.594 (0.049) |
| paper | 189.09 | RandomForest | 0.829 (0.029) | 0.541 (0.033) | 0.095 (0.021) | 0.016 (0.128) |
| paper | 194.10 | DecisionTree | 0.741 (0.030) | 0.507 (0.045) | 0.173 (0.031) | 0.226 (0.143) |
| paper | 194.10 | IRIS_Q42 | 0.713 (0.025) | 0.375 (0.016) | 0.252 (0.031) | 0.572 (0.032) |
| paper | 194.10 | QRF CV-selected | 0.713 (0.021) | 0.284 (0.029) | 0.290 (0.031) | 0.675 (0.042) |
| paper | 194.10 | QRF test-selected | 0.718 (0.021) | 0.291 (0.022) | 0.279 (0.029) | 0.686 (0.026) |
| paper | 194.10 | QRF(q=0.40) fixed | 0.711 (0.021) | 0.282 (0.029) | 0.292 (0.031) | 0.675 (0.042) |
| paper | 194.10 | QRF(q=0.45) fixed | 0.748 (0.024) | 0.338 (0.029) | 0.224 (0.029) | 0.616 (0.047) |
| paper | 194.10 | RandomForest | 0.827 (0.026) | 0.523 (0.033) | 0.101 (0.019) | 0.088 (0.118) |
| paper | train-sample P24.2 | DecisionTree | 0.738 (0.030) | 0.522 (0.045) | 0.170 (0.031) | 0.178 (0.165) |
| paper | train-sample P24.2 | IRIS_Q42 | 0.702 (0.025) | 0.387 (0.019) | 0.262 (0.031) | 0.557 (0.038) |
| paper | train-sample P24.2 | QRF CV-selected | 0.712 (0.024) | 0.298 (0.028) | 0.284 (0.029) | 0.679 (0.033) |
| paper | train-sample P24.2 | QRF test-selected | 0.712 (0.025) | 0.298 (0.025) | 0.285 (0.031) | 0.681 (0.031) |
| paper | train-sample P24.2 | QRF(q=0.40) fixed | 0.710 (0.024) | 0.297 (0.028) | 0.287 (0.029) | 0.679 (0.034) |
| paper | train-sample P24.2 | QRF(q=0.45) fixed | 0.745 (0.024) | 0.352 (0.027) | 0.223 (0.026) | 0.593 (0.046) |
| paper | train-sample P24.2 | RandomForest | 0.824 (0.028) | 0.541 (0.035) | 0.099 (0.020) | 0.020 (0.143) |

### Quantile chosen across splits (value: count)

| protocol   | threshold                              |   q_cv_mode | q_cv_values                            | q_test_values                                             |
|:-----------|:---------------------------------------|------------:|:---------------------------------------|:----------------------------------------------------------|
| disjoint   | 189.05 (IRIS recon., official ~320 Bs) |         0.4 | {0.4: np.int64(30)}                    | {0.35: np.int64(1), 0.4: np.int64(28), 0.45: np.int64(1)} |
| disjoint   | 189.09 (full-sample P24.2)             |         0.4 | {0.4: np.int64(30)}                    | {0.35: np.int64(1), 0.4: np.int64(28), 0.45: np.int64(1)} |
| disjoint   | 194.10 (IRIS recon., official ~328 Bs) |         0.4 | {0.4: np.int64(30)}                    | {0.35: np.int64(1), 0.4: np.int64(26), 0.45: np.int64(3)} |
| disjoint   | train-sample P24.2                     |         0.4 | {0.4: np.int64(29), 0.45: np.int64(1)} | {0.35: np.int64(1), 0.4: np.int64(28), 0.45: np.int64(1)} |
| paper      | 189.05 (IRIS recon., official ~320 Bs) |         0.4 | {0.4: np.int64(30)}                    | {0.35: np.int64(1), 0.4: np.int64(27), 0.45: np.int64(2)} |
| paper      | 189.09 (full-sample P24.2)             |         0.4 | {0.4: np.int64(30)}                    | {0.35: np.int64(1), 0.4: np.int64(27), 0.45: np.int64(2)} |
| paper      | 194.10 (IRIS recon., official ~328 Bs) |         0.4 | {0.4: np.int64(29), 0.45: np.int64(1)} | {0.35: np.int64(1), 0.4: np.int64(23), 0.45: np.int64(6)} |
| paper      | train-sample P24.2                     |         0.4 | {0.4: np.int64(29), 0.45: np.int64(1)} | {0.35: np.int64(1), 0.4: np.int64(27), 0.45: np.int64(2)} |
