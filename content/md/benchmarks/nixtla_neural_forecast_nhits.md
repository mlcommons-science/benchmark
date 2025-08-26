# Nixtla Neural Forecast NHITS

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2023-06-01</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">Nixtla Neural Forecast NHITS</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">Time-series; General ML</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Official NHITS implementation for long-horizon time series forecasting</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Time-series forecasting</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">RMSE, MAPE</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">NHITS</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=NHITS">NHITS</a> <a class="chip chip-link" href="../#kw=long-horizon%20forecasting">long-horizon forecasting</a> <a class="chip chip-link" href="../#kw=neural%20interpolation">neural interpolation</a> <a class="chip chip-link" href="../#kw=time-series">time-series</a> </div>
<h3>Citation</h3>

- Cristian Challu, Kin G Olivares, Boris N Oreshkin, Federico Garza Ramirez, Max Mergenthaler Canseco, and Artur Dubrawski. Nhits: neural hierarchical interpolation for time series forecasting. In Proceedings of the AAAI conference on artificial intelligence, volume 37, 6989–6997. 2023.

<pre><code class="language-bibtex">@inproceedings{challu2023nhits,
 title={Nhits: Neural hierarchical interpolation for time series forecasting},
 author={Challu, Cristian and Olivares, Kin G and Oreshkin, Boris N and Ramirez, Federico Garza and Canseco, Max Mergenthaler and Dubrawski, Artur},
 booktitle={Proceedings of the AAAI conference on artificial intelligence},
 volume={37},
 number={6},
 pages={6989--6997},
 year={2023}
 }</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Implemented within the open-source NeuralForecast library under Apache 2.0.
Includes training, evaluation, and hyperparameter tuning pipelines. Actively maintained.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">The NHITS forecasting task is clearly defined with structured input/output formats.
Model design targets long-horizon accuracy and compute efficiency.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Uses standard benchmark datasets like M4, but does not bundle them directly.
FAIR compliance depends on external dataset sources and user setup.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Evaluated using RMSE, MAPE, and other standard forecasting metrics, integrated
into training and evaluation APIs.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Official NHITS implementation is fully reproducible with training/eval configs,
though pretrained weights are not always provided.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Well-documented on GitHub and in AAAI paper, with code examples, training guidance,
and usage tutorials. More model-specific docs could improve clarity further.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.33/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="Nixtla Neural Forecast NHITS radar" src="../../../tex/images/nixtla_neural_forecast_nhits_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
