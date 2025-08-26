# Delta Squared-DFT

<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>
<div class="info-block meta-block">
  <p class="meta-row"><span class="meta-label">Date</span><span class="meta-sep">:</span> <span class="meta-value">2024-12-13</span></p>
  <p class="meta-row"><span class="meta-label">Name</span><span class="meta-sep">:</span> <span class="meta-value">Delta Squared-DFT</span></p>
  <p class="meta-row"><span class="meta-label">Domain</span><span class="meta-sep">:</span> <span class="meta-value">Computational Chemistry; Materials Science</span></p>
  <p class="meta-row"><span class="meta-label">Focus</span><span class="meta-sep">:</span> <span class="meta-value">Benchmarking machine-learning corrections to DFT using Delta Squared-trained models for reaction energies</span></p>
  <p class="meta-row"><span class="meta-label">Task Types</span><span class="meta-sep">:</span> <span class="meta-value">Regression</span></p>
  <p class="meta-row"><span class="meta-label">Metrics</span><span class="meta-sep">:</span> <span class="meta-value">Mean Absolute Error (eV), Energy ranking accuracy</span></p>
  <p class="meta-row"><span class="meta-label">Models</span><span class="meta-sep">:</span> <span class="meta-value">Delta Squared-ML correction networks, Kernel ridge regression</span></p>
</div>
<h3>Keywords</h3>

<div class="chips"><a class="chip chip-link" href="../#kw=density%20functional%20theory">density functional theory</a> <a class="chip chip-link" href="../#kw=Delta%20Squared-ML%20correction">Delta Squared-ML correction</a> <a class="chip chip-link" href="../#kw=reaction%20energetics">reaction energetics</a> <a class="chip chip-link" href="../#kw=quantum%20chemistry">quantum chemistry</a> </div>
<h3>Citation</h3>

- Kuzma Khrabrov, Anton Ber, Artem Tsypin, Konstantin Ushenin, Egor Rumiantsev, Alexander Telepov, Dmitry Protasov, Ilya Shenbin, Anton Alekseev, Mikhail Shirokikh, Sergey Nikolenko, Elena Tutubalina, and Artur Kadurin. Delta-squared dft: a universal quantum chemistry dataset of drug-like molecules and a benchmark for neural network potentials. 2024. URL: https://arxiv.org/abs/2406.14347, arXiv:2406.14347.

<pre><code class="language-bibtex">@misc{khrabrov2024nabla2dftuniversalquantumchemistry,
  title={Delta-Squared DFT: A Universal Quantum Chemistry Dataset of Drug-Like Molecules and a Benchmark for Neural Network Potentials}, 
  author={Kuzma Khrabrov and Anton Ber and Artem Tsypin and Konstantin Ushenin and Egor Rumiantsev and Alexander Telepov and Dmitry Protasov and Ilya Shenbin and Anton Alekseev and Mikhail Shirokikh and Sergey Nikolenko and Elena Tutubalina and Artur Kadurin},
  year={2024},
  eprint={2406.14347},
  archivePrefix={arXiv},
  primaryClass={physics.chem-ph},
  url={https://arxiv.org/abs/2406.14347}, 
}</code></pre>
<h3>Ratings</h3>
<div class="ratings-grid">
  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>
  <div class="rating-item">  <div class="rating-cat">Software</div>  <div class="rating-badge">3.00</div>  <div class="rating-bar"><span style="width:60%"></span></div>  <div class="rating-reason">Source code and baseline models available for ML correction to DFT; framework maturity is moderate.
</div></div><div class="rating-item">  <div class="rating-cat">Specification</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Benchmark focuses on reaction energy prediction with clear goals, though some task specifics could be formalized further.
</div></div><div class="rating-item">  <div class="rating-cat">Dataset</div>  <div class="rating-badge">4.50</div>  <div class="rating-bar"><span style="width:90%"></span></div>  <div class="rating-reason">Multi-modal quantum chemistry datasets are standardized and accessible; repository available.
</div></div><div class="rating-item">  <div class="rating-cat">Metrics</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Uses standard regression metrics like MAE and energy ranking accuracy; appropriate for task.
</div></div><div class="rating-item">  <div class="rating-cat">Reference Solution</div>  <div class="rating-badge">3.50</div>  <div class="rating-bar"><span style="width:70%"></span></div>  <div class="rating-reason">Includes baseline regression and kernel ridge models; implementations are reproducible.
</div></div><div class="rating-item">  <div class="rating-cat">Documentation</div>  <div class="rating-badge">4.00</div>  <div class="rating-bar"><span style="width:80%"></span></div>  <div class="rating-reason">Source code supports pipeline reuse, but formal evaluation splits may vary.
</div></div>
</div>
<div class="avg-rating">  <strong>Average rating:</strong> <span class="badge badge--meh badge--sm">3.83/5</span></div><h3>Radar plot</h3>

<div class="radar-wrap"><img class="radar-img" alt="Delta Squared-DFT radar" src="../../../tex/images/delta_squared-dft_radar.png" /></div>

<p><strong>Edit:</strong> <a href="https://github.com/mlcommons-science/benchmark/tree/main/source">edit this entry</a></p>
