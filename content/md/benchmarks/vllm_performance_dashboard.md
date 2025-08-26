# vLLM Performance Dashboard

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2022-06-22</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">vLLM Performance Dashboard</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">LLM; HPC/inference</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Interactive dashboard showing inference performance of vLLM</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Performance visualization</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Tokens/sec, TTFT, Memory usage</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">LLaMA-2, Mistral, Qwen</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=Dashboard">Dashboard</a> <a class="chip chip-link" href="../#kw=Throughput%20visualization">Throughput visualization</a> <a class="chip chip-link" href="../#kw=Latency%20analysis">Latency analysis</a> <a class="chip chip-link" href="../#kw=Metric%20tracking">Metric tracking</a> </div>
<h3>Citation</h3>

- Simon Mo. Vllm performance dashboard. 2024. URL: https://simon-mo-workspace.observablehq.cloud/vllm-dashboard-v0/.

<pre><code class="language-bibtex">@misc{mo2024vllm_dashboard,
  title={vLLM Performance Dashboard},
  author={Mo, Simon},
  year={2024},
  url={https://simon-mo-workspace.observablehq.cloud/vllm-dashboard-v0/}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Interactive dashboard built with ObservableHQ and linked to vLLM benchmarks.
Source code is not fully open, but backend integration with vLLM is well-maintained.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">While primarily a visualization tool, it includes benchmark configurations,
metric definitions, and supports comparison across models and hardware.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">2.00</div>  <div class="rating-bar"><span style="width:40%"></span></div>  <div class="rating-reason">No datasets are bundled; the dashboard visualizes metrics derived from model
inference logs or external endpoints, not a formal dataset.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Tracks tokens/sec, TTFT, memory usage, and platform comparisons. Metrics are clear
but focused on visualization rather than statistical robustness.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Dashboards include reproducible views of benchmarked models, but do not ship
with runnable model code. Relies on external serving infrastructure.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Public dashboard with instructions and tooltips; documentation is clear, though access
is restricted (login required) and backend setup is opaque to users.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--meh badge--sm">3.50/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="vLLM Performance Dashboard radar" src="../../../tex/images/vllm_performance_dashboard_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
