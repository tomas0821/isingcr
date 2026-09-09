#!/usr/bin/env python3
"""Two reader-facing tables for the Supplementary Material, from data already
on disk (no MC): the 15 most contested distritos (highest multistability
score = min(error rate, 1 - error rate) across the 16 pooled seeds of the
2026 GAM fit) and the 15 worst-predicted distritos (highest per-node error
rate), each with province, canton, GAM-proxy status, GAM-boundary status,
and the MIDEPLAN IDS z-score. Source: data/processed/
gam_domain_wall_analysis_2026.csv + the IDS field from run_3d_scan.
Writes manuscript/contested_tables.tex (\\input-able) and prints it.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from run_3d_scan import build_distrito_graph_and_fields  # noqa: E402

df = pd.read_csv(ROOT / "data" / "processed" / "gam_domain_wall_analysis_2026.csv")
_, _, ids, nodes, emp = build_distrito_graph_and_fields()
idsmap = dict(zip(nodes, ids)); empmap = dict(zip(nodes, emp))
lead = 1 if np.mean(emp == 1) > 0.5 else -1
df["ids_z"] = df["node"].map(idsmap)
df["side"] = df["node"].map(lambda n: "leading" if empmap[n] == lead else "coalition")
df["multistability"] = np.minimum(df["error_rate"], 1 - df["error_rate"])
df[["prov", "canton", "distrito"]] = df["node"].str.split("|", expand=True)


def title(s):
    return s.title().replace(" De ", " de ").replace(" Del ", " del ").replace(" La ", " la ").replace(" Y ", " y ")


def tex_table(sub, score_col, score_label, caption, label):
    lines = [r"\begin{table*}[htbp]", r"\centering", r"\caption{" + caption + "}", r"\label{" + label + "}",
             r"\begin{tabular}{llllcccr}", r"\toprule",
             r"Province & Canton & Distrito & Real side & GAM proxy & GAM boundary & IDS $z$ & " + score_label + r" \\",
             r"\midrule"]
    for _, r in sub.iterrows():
        lines.append(f"{title(r.prov)} & {title(r.canton)} & {title(r.distrito)} & {r.side} & "
                     f"{'yes' if r.is_gam else 'no'} & {'yes' if r.is_boundary else 'no'} & "
                     f"${r.ids_z:+.2f}$ & ${r[score_col]:.3f}$ \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
    return "\n".join(lines)


top_ms = df[df["multistability"] >= 0.1875].sort_values(["multistability", "error_rate"], ascending=False)
t1 = tex_table(top_ms, "multistability", "Multistability",
               "The " + str(len(top_ms)) + " contested distritos under the fitted 2026 geography+GAM model: "
               "every distrito with multistability score $=\\min(\\text{error rate}, 1-\\text{error rate}) "
               "\\geq 3/16$ across the 16 pooled seeds at $T=1.008$ (0.5 would be an even 8--8 split). "
               "``Real side'' is the distrito's actual 2026 outcome; ``GAM boundary'' marks a distrito with "
               "at least one neighbor of the opposite GAM-proxy status; IDS $z$ is the MIDEPLAN composite. "
               "Place names follow the accent-stripped TSE export.",
               "tab:contested")
# always-wrong distritos, aggregated by canton
aw = df[df["error_rate"] == 1.0]
tot = df.groupby(["prov", "canton"]).size().rename("n_total")
g = aw.groupby(["prov", "canton"]).agg(n_wrong=("node", "size"), gam=("is_gam", "max"),
                                       side=("side", lambda x: x.mode().iat[0]),
                                       ids=("ids_z", "mean")).join(tot).reset_index()
g = g.sort_values(["n_wrong", "prov"], ascending=[False, True])
lines = [r"\begin{table*}[htbp]", r"\centering",
         r"\caption{The " + str(len(aw)) + r" distritos the fitted 2026 geography+GAM model gets wrong in every one "
         r"of the 16 pooled seeds, aggregated by canton (" + str(len(g)) + r" cantons). ``Real side'' is the "
         r"majority actual outcome among the canton's always-wrong distritos; IDS $z$ is their mean. "
         r"Alajuela's central canton and the Los Santos coffee highlands (Tarraz\'u, Dota, Le\'on Cort\'es) "
         r"account for 25 of the 69.}",
         r"\label{tab:alwayswrong}", r"\begin{tabular}{llcccc}", r"\toprule",
         r"Province & Canton & Always wrong / total & GAM proxy & Real side & mean IDS $z$ \\", r"\midrule"]
for _, r in g.iterrows():
    lines.append(f"{title(r.prov)} & {title(r.canton)} & {int(r.n_wrong)} / {int(r.n_total)} & "
                 f"{'yes' if r.gam else 'no'} & {r.side} & ${r.ids:+.2f}$ \\\\")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
t2 = "\n".join(lines)
out = ROOT / "manuscript" / "contested_tables.tex"
out.write_text(t1 + "\n\n" + t2 + "\n", encoding="utf-8")
print(t2)
print("\nLos Santos (Tarrazu+Dota+Leon Cortes) always-wrong:", int(aw[aw.canton.isin(["TARRAZU","DOTA","LEON CORTES CASTRO"])].shape[0]),
      " Alajuela Central:", int(aw[(aw.prov=="ALAJUELA")&(aw.canton=="CENTRAL")].shape[0]))
