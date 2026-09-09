#!/usr/bin/env python3
"""SM table: the 24 distritos the 31-canton proxy labels GAM whose area-majority
lies outside the official Plan GAM polygon, with their fraction inside, real
2026 side, and error rate under the proxy model; plus the per-canton summary."""
import numpy as np, pandas as pd
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
fr = pd.read_csv(ROOT / "data/processed/gam_distrito_fraction_2026.csv")
err = pd.read_csv(ROOT / "data/processed/gam_domain_wall_analysis_2026.csv")[["node", "error_rate"]]
fr = fr.merge(err, on="node", how="left")
lead = 1 if (fr.empirical == 1).mean() > 0.5 else -1
fr["side"] = np.where(fr.empirical == lead, "leading", "coalition")
fr[["prov", "canton", "distrito"]] = fr["node"].str.split("|", expand=True)
def title(s): return s.title().replace(" De ", " de ").replace(" Del ", " del ")
po = fr[fr.proxy & ~fr.gam_majority].sort_values(["prov", "canton", "frac_in_gam"])
L = [r"\begin{table*}[htbp]", r"\centering\small",
     r"\caption{The 24 distritos that the 31-canton proxy labels GAM but whose area-majority lies outside the official Plan GAM 2013--2030 polygon (\emph{fraction}: share of the distrito's area inside the polygon). ``Side'' is the real 2026 outcome; ``error'' is the per-node error rate under the proxy-field model (16 seeds). Eleven of the 24 are on the leading (periphery-like) side, against $29.6\%$ of the 162 distritos inside the polygon; three are always wrong under the proxy model. Alajuela's central canton contributes one distrito (Sarapiqu\'i); its other 13 distritos lie inside the polygon.}",
     r"\label{tab:gam-boundary}", r"\begin{tabular}{lllrlr}", r"\toprule",
     r"Province & Canton & Distrito & Fraction & Side & Error \\", r"\midrule"]
for _, r in po.iterrows():
    L.append(f"{title(r.prov)} & {title(r.canton)} & {title(r.distrito)} & {r.frac_in_gam:.3f} & {r.side} & {r.error_rate:.2f} \\\\")
L += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
(ROOT / "manuscript" / "gam_boundary_table.tex").write_text("\n".join(L) + "\n", encoding="utf-8")
print("rows", len(po), "leading share", np.mean(po.side == "leading").round(3), "always wrong", int((po.error_rate >= 0.999).sum()))
print("inside 162: leading share", np.mean(fr[fr.gam_majority].side == "leading").round(3))
print("by canton:", po.groupby("canton").size().to_dict())
