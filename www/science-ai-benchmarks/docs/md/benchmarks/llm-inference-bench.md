# LLM-Inference-Bench

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2024-10-31</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">LLM-Inference-Bench</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">LLM; HPC/inference</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Hardware performance benchmarking of LLMs on AI accelerators</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Inference Benchmarking</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Token throughput (tok/s), Latency, Framework-hardware mix performance</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">LLaMA-2-7B, LLaMA-2-70B, Mistral-7B, Qwen-7B</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=LLM">LLM</a> <a class="chip chip-link" href="../#kw=inference%20benchmarking">inference benchmarking</a> <a class="chip chip-link" href="../#kw=GPU">GPU</a> <a class="chip chip-link" href="../#kw=accelerator">accelerator</a> <a class="chip chip-link" href="../#kw=throughput">throughput</a> </div>
<h3>Citation</h3>

- Krishna Teja Chitty-Venkata, Siddhisanket Raskar, Bharat Kale, Farah Ferdaus, Aditya Tanikanti, Ken Raffenetti, Valerie Taylor, Murali Emani, and Venkatram Vishwanath. Llm-inference-bench: inference benchmarking of large language models on ai accelerators. In SC24-W: Workshops of the International Conference for High Performance Computing, Networking, Storage and Analysis, volume, 1362 1379. 2024. doi:10.1109/SCW63240.2024.00178.

<pre><code class="language-bibtex">@INPROCEEDINGS{10820566,
  author={Chitty-Venkata, Krishna Teja and Raskar, Siddhisanket and Kale, Bharat and Ferdaus, Farah and Tanikanti, Aditya and Raffenetti, Ken and Taylor, Valerie and Emani, Murali and Vishwanath, Venkatram},
  booktitle={SC24-W: Workshops of the International Conference for High Performance Computing, Networking, Storage and Analysis}, 
  title={LLM-Inference-Bench: Inference Benchmarking of Large Language Models on AI Accelerators}, 
  year={2024},
  volume={},
  number={},
  pages={1362-1379},
  keywords={Performance evaluation;Power demand;Computational modeling;Large language models;Scalability;High performance computing;AI accelerators;Benchmark testing;Propulsion;Throughput;Large Language Models;AI Accelerators;Inference Performance Evaluation;Benchmarking},
  doi={10.1109/SCW63240.2024.00178}}
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Public GitHub repository (https://github.com/argonne-lcf/LLM-Inference-Bench) under BSD-3 license.
Includes scripts, configurations, and dashboards for running and visualizing LLM inference benchmarks
across multiple accelerator platforms.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Benchmark scope, models, accelerator targets, and supported frameworks are clearly specified.
Input configurations and output metrics are standardized across hardware types.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">2.00</div>  <div class="rating-bar"><span style="width:40%"></span></div>  <div class="rating-reason">No novel dataset is introduced; benchmark relies on pre-trained LLMs and synthetic inference inputs.
Dataset structure and FAIR considerations are minimal.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">5.00</div>  <div class="rating-bar"><span style="width:100%"></span></div>  <div class="rating-reason">Hardware-specific metrics (token throughput, latency, utilization) are well-defined, consistently measured,
and aggregated in dashboards.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Inference configurations and baseline performance results are provided, but there are no
full reference training pipelines or model implementations.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">GitHub repo provides clear usage instructions, setup guides, and interactive dashboard tooling.
Some areas like benchmarking extensions or advanced tuning are less detailed.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--ok badge--sm">4.00/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="LLM-Inference-Bench radar" src="../../../tex/images/llm-inference-bench_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
