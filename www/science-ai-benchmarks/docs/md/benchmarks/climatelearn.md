# ClimateLearn

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2023-07-19</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">ClimateLearn</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">Climate Science; Forecasting</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">ML for weather and climate modeling</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Forecasting</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">RMSE, Anomaly correlation</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">CNN baselines, ResNet variants</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=medium-range%20forecasting">medium-range forecasting</a> <a class="chip chip-link" href="../#kw=ERA5">ERA5</a> <a class="chip chip-link" href="../#kw=data-driven">data-driven</a> </div>
<h3>Citation</h3>

- Tung Nguyen, Jason Jewik, Hritik Bansal, Prakhar Sharma, and Aditya Grover. Climatelearn: benchmarking machine learning for weather and climate modeling. 2023. URL: https://arxiv.org/abs/2307.01909, arXiv:2307.01909.

<pre><code class="language-bibtex">@misc{nguyen2023climatelearnbenchmarkingmachinelearning, 
  title={ClimateLearn: Benchmarking Machine Learning for Weather and Climate Modeling}, 
  author={Tung Nguyen and Jason Jewik and Hritik Bansal and Prakhar Sharma and Aditya Grover},
  year={2023}, eprint={2307.01909}, 
  archivePrefix={arXiv}, 
  primaryClass={cs.LG},
  url={https://arxiv.org/abs/2307.01909}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Quickstart notebook makes for easy usage
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Task framing (medium-range climate forecasting), input/output formats, and evaluation windows are clearly defined; benchmark supports both physical and learned models with detailed constraints.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Provides standardized access to ERA5 and other reanalysis datasets, with ML-ready splits, metadata, and Xarray-compatible formats; versioned and fully FAIR-compliant.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">ACC and RMSE are standard, quantitative, and appropriate for climate forecasting; well-integrated into the benchmark, though interpretation across domains may vary.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">0.00</div>  <div class="rating-bar"><span style="width:0%"></span></div>  <div class="rating-reason">The benchmark is geared for CNN architectures, but no specific model was mentioned.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Explained in the benchmark&#x27;s paper. 
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.17/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="ClimateLearn radar" src="../../../tex/images/climatelearn_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
