#!/usr/bin/env python3
"""
Project 1, step 2: answer the business questions from the cleaned session table.

    python 02_analysis.py

Reads   ../data/cleaned/sessions.csv, ../data/cleaned/ad_spend.csv
Writes  output/*.csv          one table per question (the SQL in ../sql/ reproduces each one)
        output/findings.json  the headline numbers, significance checks and sizing estimates
        figures/*.png         the charts used in the README and the report

Rates are always written with both ends named:
    begin rate      = sessions that started the sign-up form / sessions
    OTP rate        = sessions that verified their phone / sessions that started the form
    completion rate = sessions that finished sign-up / sessions that verified their phone
    conversion      = sessions that finished sign-up / sessions
"""
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import PathPatch  # noqa: E402
from matplotlib.path import Path as MplPath  # noqa: E402
from matplotlib.transforms import IdentityTransform  # noqa: E402

HERE = Path(__file__).resolve().parent
CLEAN = HERE.parent / "data" / "cleaned"
OUT, FIG = HERE / "output", HERE / "figures"
PAID = ["Paid Search", "Paid Social"]
INCIDENT = ("2026-05-18", "2026-05-29")
PERIOD_LABEL = "30 Mar to 28 Jun 2026"


def pct(num, den, nd=2):
    return round(100.0 * num / den, nd) if den else None


def funnel(df: pd.DataFrame) -> dict:
    s, b, o, c = len(df), int(df["began_signup"].sum()), int(df["otp_verified"].sum()), int(df["signed_up"].sum())
    return {"sessions": s, "began_signup": b, "otp_verified": o, "signed_up": c, "begin_rate_pct": pct(b, s),
            "otp_rate_pct": pct(o, b), "completion_rate_pct": pct(c, o), "conversion_pct": pct(c, s)}


def two_proportions(x1, n1, x2, n2) -> dict:
    """Two-sided z-test for a difference between two proportions, with a 95% interval for the difference."""
    p1, p2 = x1 / n1, x2 / n2
    pooled = (x1 + x2) / (n1 + n2)
    se_pooled = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se_pooled
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return {"p1_pct": round(100 * p1, 2), "n1": int(n1), "p2_pct": round(100 * p2, 2), "n2": int(n2),
            "diff_pts": round(100 * (p1 - p2), 2),
            "ci95_pts": [round(100 * (p1 - p2 - 1.96 * se), 2), round(100 * (p1 - p2 + 1.96 * se), 2)],
            "z": round(z, 2), "p_value": float(f"{math.erfc(abs(z) / math.sqrt(2)):.2g}")}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    FIG.mkdir(exist_ok=True)
    s = pd.read_csv(CLEAN / "sessions.csv", dtype={"user_pseudo_id": str})
    spend = pd.read_csv(CLEAN / "ad_spend.csv")
    f = {"period": PERIOD_LABEL}
    total_sessions, total_signups, total_cost = len(s), int(s["signed_up"].sum()), float(spend["cost_ghs"].sum())

    # ------------------------------------------------------------------ KPI summary
    paid_signups = int(s.loc[s["channel_group"].isin(PAID), "signed_up"].sum())
    kpi = {"sessions": total_sessions, "users": int(s["user_pseudo_id"].nunique()), "signups": total_signups,
           "conversion_pct": pct(total_signups, total_sessions), "engaged_rate_pct": pct(s["engaged_session"].sum(), total_sessions),
           "new_user_session_pct": pct(s["is_new_user"].sum(), total_sessions),
           "begin_rate_pct": pct(s["began_signup"].sum(), total_sessions),
           "otp_rate_pct": pct(s["otp_verified"].sum(), s["began_signup"].sum()),
           "completion_rate_pct": pct(total_signups, s["otp_verified"].sum()),
           "cost_ghs": round(total_cost, 2), "paid_signups": paid_signups,
           "cost_per_paid_signup": round(total_cost / paid_signups, 2)}
    pd.DataFrame([kpi]).to_csv(OUT / "kpi_summary.csv", index=False)
    f["kpi"] = kpi

    # ------------------------------------------------------------------ Q1 channels
    ch = s.groupby("channel_group").agg(sessions=("signed_up", "size"), signups=("signed_up", "sum"),
                                        began=("began_signup", "sum")).reset_index()
    cost_ch = spend.groupby("channel_group")["cost_ghs"].sum()
    ch["session_share_pct"] = (100 * ch["sessions"] / total_sessions).round(2)
    ch["signup_share_pct"] = (100 * ch["signups"] / total_signups).round(2)
    ch["begin_rate_pct"] = (100 * ch["began"] / ch["sessions"]).round(2)
    ch["conversion_pct"] = (100 * ch["signups"] / ch["sessions"]).round(2)
    ch["cost_ghs"] = ch["channel_group"].map(cost_ch).round(2)
    ch["cost_per_signup"] = (ch["cost_ghs"] / ch["signups"]).round(2)
    ch = ch.sort_values("sessions", ascending=False)[["channel_group", "sessions", "session_share_pct", "signups", "signup_share_pct",
                                                      "begin_rate_pct", "conversion_pct", "cost_ghs", "cost_per_signup"]]
    ch.to_csv(OUT / "channel_performance.csv", index=False)
    f["channels"] = ch.to_dict("records")

    # ------------------------------------------------------------------ Q1b campaigns
    cs = spend.groupby(["campaign", "platform"]).agg(clicks=("clicks", "sum"), cost_ghs=("cost_ghs", "sum")).reset_index()
    sess_c = s.groupby("campaign").agg(sessions=("signed_up", "size"), signups=("signed_up", "sum"))
    camp = cs.join(sess_c, on="campaign")
    camp["cost_ghs"] = camp["cost_ghs"].round(2)
    camp["cpc_ghs"] = (camp["cost_ghs"] / camp["clicks"]).round(2)
    camp["conversion_pct"] = (100 * camp["signups"] / camp["sessions"]).round(2)
    camp["cost_per_signup"] = (camp["cost_ghs"] / camp["signups"]).round(2)
    camp = camp.sort_values("cost_per_signup", ascending=False)[["campaign", "platform", "clicks", "cost_ghs", "cpc_ghs", "sessions",
                                                                 "signups", "conversion_pct", "cost_per_signup"]]
    camp.to_csv(OUT / "campaign_performance.csv", index=False)
    f["campaigns"] = camp.to_dict("records")
    f["unattributed_paid_sessions"] = int((s["campaign"] == "(unattributed)").sum())

    # ------------------------------------------------------------------ Q2 funnel by device
    dev = pd.DataFrame([{"device_category": d, **funnel(g)} for d, g in s.groupby("device_category")])
    dev = dev.sort_values("sessions", ascending=False)
    dev.to_csv(OUT / "funnel_by_device.csv", index=False)
    f["funnel_all"] = funnel(s)
    f["funnel_by_device"] = dev.to_dict("records")
    mob, desk, tab = (s[s["device_category"] == d] for d in ("mobile", "desktop", "tablet"))
    f["test_mobile_vs_desktop_completion"] = two_proportions(mob["signed_up"].sum(), mob["otp_verified"].sum(),
                                                             desk["signed_up"].sum(), desk["otp_verified"].sum())
    mob_verified, mob_done = int(mob["otp_verified"].sum()), int(mob["signed_up"].sum())
    desk_rate = desk["signed_up"].sum() / desk["otp_verified"].sum()
    tab_rate = tab["signed_up"].sum() / tab["otp_verified"].sum()
    f["sizing_mobile_form"] = {
        "mobile_sessions_share_pct": pct(len(mob), total_sessions), "mobile_verified": mob_verified, "mobile_completed": mob_done,
        "mobile_abandoned_after_otp": mob_verified - mob_done,
        "extra_signups_at_tablet_rate": int(round(mob_verified * tab_rate - mob_done)),
        "extra_signups_at_desktop_rate": int(round(mob_verified * desk_rate - mob_done)),
        "extra_signups_closing_half_the_gap": int(round((mob_verified * desk_rate - mob_done) / 2)),
        "as_pct_of_all_signups_half_gap": pct((mob_verified * desk_rate - mob_done) / 2, total_signups, 1),
    }

    # ------------------------------------------------------------------ Q3 landing pages
    lp = s.groupby("landing_page").agg(sessions=("signed_up", "size"), engaged=("engaged_session", "sum"),
                                       began=("began_signup", "sum"), signups=("signed_up", "sum")).reset_index()
    lp["bounce_rate_pct"] = (100 - 100 * lp["engaged"] / lp["sessions"]).round(2)
    lp["begin_rate_pct"] = (100 * lp["began"] / lp["sessions"]).round(2)
    lp["conversion_pct"] = (100 * lp["signups"] / lp["sessions"]).round(2)
    lp = lp.sort_values("sessions", ascending=False)[["landing_page", "sessions", "bounce_rate_pct", "begin_rate_pct", "signups", "conversion_pct"]]
    lp.to_csv(OUT / "landing_pages.csv", index=False)
    f["landing_pages"] = lp.to_dict("records")

    is_cb = s["landing_page"] == "/promo/cashback"
    rows = []
    for g, d in s.groupby("channel_group"):
        on, off = d[d["landing_page"] == "/promo/cashback"], d[d["landing_page"] != "/promo/cashback"]
        if len(on) >= 100:
            rows.append({"channel_group": g, "cashback_sessions": len(on), "cashback_conversion_pct": pct(on["signed_up"].sum(), len(on)),
                         "other_sessions": len(off), "other_conversion_pct": pct(off["signed_up"].sum(), len(off))})
    cb = pd.DataFrame(rows).sort_values("cashback_sessions", ascending=False)
    cb.to_csv(OUT / "cashback_page_by_channel.csv", index=False)
    f["cashback_by_channel"] = cb.to_dict("records")
    f["cashback_page"] = {"sessions": int(is_cb.sum()), "session_share_pct": pct(is_cb.sum(), total_sessions),
                          "signups": int(s.loc[is_cb, "signed_up"].sum()),
                          "conversion_pct": pct(s.loc[is_cb, "signed_up"].sum(), is_cb.sum()),
                          "rest_of_site_conversion_pct": pct(s.loc[~is_cb, "signed_up"].sum(), (~is_cb).sum())}
    em = s[s["channel_group"] == "Email"]
    f["test_cashback_within_email"] = two_proportions(em.loc[em["landing_page"] == "/promo/cashback", "signed_up"].sum(),
                                                      (em["landing_page"] == "/promo/cashback").sum(),
                                                      em.loc[em["landing_page"] != "/promo/cashback", "signed_up"].sum(),
                                                      (em["landing_page"] != "/promo/cashback").sum())
    spark, campus = s[s["campaign"] == "TT_Spark_CashbackChallenge"], s[s["campaign"] == "TT_InFeed_CampusAmbassadors"]
    f["test_spark_vs_campus_conversion"] = two_proportions(spark["signed_up"].sum(), len(spark), campus["signed_up"].sum(), len(campus))
    spark_cost = float(spend.loc[spend["campaign"] == "TT_Spark_CashbackChallenge", "cost_ghs"].sum())
    campus_rate = campus["signed_up"].sum() / len(campus)
    f["sizing_cashback_page"] = {
        "spark_sessions": len(spark), "spark_cost_ghs": round(spark_cost, 2), "spark_signups": int(spark["signed_up"].sum()),
        "spark_cost_per_signup": round(spark_cost / spark["signed_up"].sum(), 2),
        "signups_at_campus_rate": int(round(len(spark) * campus_rate)),
        "signups_at_half_campus_rate": int(round(len(spark) * campus_rate / 2)),
        "cost_per_signup_at_half_campus_rate": round(spark_cost / (len(spark) * campus_rate / 2), 2),
    }

    # ------------------------------------------------------------------ Q4 geography
    rem = s[s["campaign"] == "META_Lookalike_Remitters"]
    rc = pd.DataFrame([{"country": c, "sessions": len(g), "session_share_pct": pct(len(g), len(rem)),
                        "began_signup": int(g["began_signup"].sum()), "otp_verified": int(g["otp_verified"].sum()),
                        "signups": int(g["signed_up"].sum()), "conversion_pct": pct(g["signed_up"].sum(), len(g))}
                       for c, g in rem.groupby("country")]).sort_values("sessions", ascending=False)
    rc.to_csv(OUT / "remitters_by_country.csv", index=False)
    f["remitters_by_country"] = rc.to_dict("records")
    rem_cost = float(spend.loc[spend["campaign"] == "META_Lookalike_Remitters", "cost_ghs"].sum())
    abroad = rem[rem["country"] != "Ghana"]
    home = rem[rem["country"] == "Ghana"]
    f["sizing_remitters"] = {
        "cost_ghs": round(rem_cost, 2), "sessions": len(rem), "abroad_sessions": len(abroad),
        "abroad_share_pct": pct(len(abroad), len(rem), 1), "abroad_signups": int(abroad["signed_up"].sum()),
        "abroad_begin_rate_pct": pct(abroad["began_signup"].sum(), len(abroad)),
        "abroad_otp_rate_pct": pct(abroad["otp_verified"].sum(), abroad["began_signup"].sum()),
        "ghana_conversion_pct": pct(home["signed_up"].sum(), len(home)),
        "spend_on_abroad_clicks_ghs": round(rem_cost * len(abroad) / len(rem), 2),
        "cost_per_signup_now": round(rem_cost / rem["signed_up"].sum(), 2),
        "cost_per_signup_ghana_only": round(rem_cost * len(home) / len(rem) / home["signed_up"].sum(), 2),
    }
    f["test_remitters_abroad_vs_ghana_conversion"] = two_proportions(abroad["signed_up"].sum(), len(abroad),
                                                                     home["signed_up"].sum(), len(home))
    all_abroad = s[s["country"] != "Ghana"]
    f["abroad_all_channels"] = {"sessions": len(all_abroad), "session_share_pct": pct(len(all_abroad), total_sessions),
                                "began_signup": int(all_abroad["began_signup"].sum()),
                                "begin_rate_pct": pct(all_abroad["began_signup"].sum(), len(all_abroad)),
                                "signups": int(all_abroad["signed_up"].sum()),
                                "conversion_pct": pct(all_abroad["signed_up"].sum(), len(all_abroad))}

    gh = s[s["country"] == "Ghana"]
    reg = gh.groupby("region").agg(sessions=("signed_up", "size"), signups=("signed_up", "sum"),
                                   paid=("channel_group", lambda x: int(x.isin(PAID).sum()))).reset_index()
    reg["conversion_pct"] = (100 * reg["signups"] / reg["sessions"]).round(2)
    reg["paid_share_pct"] = (100 * reg["paid"] / reg["sessions"]).round(2)
    reg = reg.sort_values("sessions", ascending=False)[["region", "sessions", "signups", "conversion_pct", "paid_share_pct"]]
    reg.to_csv(OUT / "ghana_regions.csv", index=False)
    f["ghana_regions"] = reg.to_dict("records")
    # Averages hide mix: Accra gets more low-converting paid social. Re-weight each region to Accra's channel mix.
    accra, ash = gh[gh["region"] == "Greater Accra"], gh[gh["region"] == "Ashanti"]
    weights = accra["channel_group"].value_counts(normalize=True)
    rows = []
    for name, d in (("Greater Accra", accra), ("Ashanti", ash)):
        by_ch = d.groupby("channel_group")["signed_up"].mean()
        rows.append({"region": name, "sessions": len(d), "conversion_pct": pct(d["signed_up"].sum(), len(d)),
                     "paid_share_pct": pct(d["channel_group"].isin(PAID).sum(), len(d)),
                     "conversion_at_accra_mix_pct": round(100 * float((by_ch * weights).sum()), 2)})
    adj = pd.DataFrame(rows)
    adj.to_csv(OUT / "region_mix_adjusted.csv", index=False)
    f["region_mix_adjusted"] = rows
    f["test_ashanti_vs_accra_conversion"] = two_proportions(ash["signed_up"].sum(), len(ash), accra["signed_up"].sum(), len(accra))
    paid_gh = gh[gh["channel_group"].isin(PAID)]
    f["paid_sessions_by_region_share_pct"] = {r: pct((paid_gh["region"] == r).sum(), len(paid_gh), 1) for r in ("Greater Accra", "Ashanti")}

    # ------------------------------------------------------------------ Q5 the iOS OTP incident
    # Ghana only: visitors abroad cannot pass OTP at all, and they are far more often on iOS.
    mobile_os = gh[gh["operating_system"].isin(["iOS", "Android"])]
    wk = mobile_os.groupby(["operating_system", "week_start"]).agg(began_signup=("began_signup", "sum"),
                                                                   otp_verified=("otp_verified", "sum")).reset_index()
    wk["otp_rate_pct"] = (100 * wk["otp_verified"] / wk["began_signup"]).round(2)
    wk["prev4_avg_rate_pct"] = (wk.groupby("operating_system")["otp_rate_pct"]
                                .transform(lambda r: r.shift(1).rolling(4, min_periods=1).mean()).round(2))
    wk["change_vs_prev4_pts"] = (wk["otp_rate_pct"] - wk["prev4_avg_rate_pct"]).round(2)
    wk = wk.sort_values(["week_start", "operating_system"])[["week_start", "operating_system", "began_signup", "otp_verified",
                                                             "otp_rate_pct", "prev4_avg_rate_pct", "change_vs_prev4_pts"]]
    wk.to_csv(OUT / "otp_rate_weekly_by_os.csv", index=False)

    ios = gh[gh["operating_system"] == "iOS"]
    in_win = ios["session_date"].between(*INCIDENT)
    b_in, o_in = int(ios.loc[in_win, "began_signup"].sum()), int(ios.loc[in_win, "otp_verified"].sum())
    b_out, o_out = int(ios.loc[~in_win, "began_signup"].sum()), int(ios.loc[~in_win, "otp_verified"].sum())
    ios_completion = ios.loc[~in_win, "signed_up"].sum() / o_out
    expected_otp = b_in * o_out / b_out
    lost = (expected_otp - o_in) * ios_completion
    win_all = s[s["session_date"].between(*INCIDENT)]
    prior = s[s["session_date"].between("2026-05-04", "2026-05-17")]
    andr = gh[gh["operating_system"] == "Android"]
    a_in = andr["session_date"].between(*INCIDENT)
    f["incident_ios_otp"] = {
        "window": list(INCIDENT), "days": 12,
        "ios_begins_in_window": b_in, "ios_otp_in_window": o_in, "ios_otp_rate_in_window_pct": pct(o_in, b_in, 1),
        "ios_otp_rate_outside_pct": pct(o_out, b_out, 1),
        "android_otp_rate_in_window_pct": pct(andr.loc[a_in, "otp_verified"].sum(), andr.loc[a_in, "began_signup"].sum(), 1),
        "android_otp_rate_outside_pct": pct(andr.loc[~a_in, "otp_verified"].sum(), andr.loc[~a_in, "began_signup"].sum(), 1),
        "expected_otp_in_window": round(expected_otp, 1), "ios_completion_rate_pct": round(100 * float(ios_completion), 1),
        "estimated_lost_signups": int(round(lost)),
        "signups_in_window": int(win_all["signed_up"].sum()),
        "lost_as_pct_of_window_signups": pct(lost, win_all["signed_up"].sum() + lost, 1),
        "site_conversion_in_window_pct": pct(win_all["signed_up"].sum(), len(win_all)),
        "site_conversion_prior_fortnight_pct": pct(prior["signed_up"].sum(), len(prior)),
        "ios_share_of_ghana_sessions_pct": pct(len(ios), len(gh), 1),
        "test": two_proportions(o_in, b_in, o_out, b_out),
    }

    # ------------------------------------------------------------------ supporting cuts
    nr = s.groupby("is_new_user").agg(sessions=("signed_up", "size"), signups=("signed_up", "sum")).reset_index()
    nr["visitor_type"] = nr["is_new_user"].map({1: "new", 0: "returning"})
    nr["conversion_pct"] = (100 * nr["signups"] / nr["sessions"]).round(2)
    nr[["visitor_type", "sessions", "signups", "conversion_pct"]].to_csv(OUT / "new_vs_returning.csv", index=False)
    f["new_vs_returning"] = nr[["visitor_type", "sessions", "signups", "conversion_pct"]].to_dict("records")

    wt = s.groupby("week_start").agg(sessions=("signed_up", "size"), signups=("signed_up", "sum")).reset_index()
    wt["conversion_pct"] = (100 * wt["signups"] / wt["sessions"]).round(2)
    wt["cost_ghs"] = wt["week_start"].map(spend.groupby("week_start")["cost_ghs"].sum()).round(2)
    wt.to_csv(OUT / "weekly_trend.csv", index=False)
    f["weekly_trend"] = wt.to_dict("records")

    (OUT / "findings.json").write_text(json.dumps(f, indent=2, default=float) + "\n", encoding="ascii")
    charts(ch, dev, lp, wk, camp)
    print(f"wrote {len(list(OUT.glob('*.csv')))} tables, findings.json and {len(list(FIG.glob('*.png')))} figures")


# ---------------------------------------------------------------------------------------------- charts
# Colours and mark sizes follow one small system: a light surface, grey text tokens, one blue for the
# series that carries the story, grey for context. Sizes are in CSS pixels (1 px = 1/96 inch).
SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, BLUE_LIGHT, BLUE_DARK, ORANGE, CONTEXT = "#2a78d6", "#86b6ef", "#1c5cab", "#eb6834", "#c3c2b7"
DPI = 192
PX = 72 / 96            # points per CSS pixel


def new_fig(height_px, left=0.30, right=0.96, top_px=92, bottom_px=64, width_px=880):
    plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 13 * PX, "text.color": INK,
                         "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED})
    fig = plt.figure(figsize=(width_px / 96, height_px / 96), dpi=DPI, facecolor=SURFACE)
    ax = fig.add_axes([left, bottom_px / height_px, right - left, 1 - (top_px + bottom_px) / height_px], facecolor=SURFACE)
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0, labelsize=12 * PX)
    return fig, ax


def titles(fig, title, subtitle, height_px, source="Source: CediFlow web sessions (synthetic data), " + PERIOD_LABEL):
    fig.text(0.03, 1 - 30 / height_px, title, fontsize=16 * PX, fontweight="semibold", color=INK, va="center")
    fig.text(0.03, 1 - 54 / height_px, subtitle, fontsize=12.5 * PX, color=INK2, va="center")
    fig.text(0.03, 16 / height_px, source, fontsize=11 * PX, color=MUTED, va="center")


def bar(ax, base, tip, pos, color, horizontal=True, thick_px=18, r_px=4):
    """One bar, square at the baseline and rounded at the data end, drawn in device pixels."""
    k = ax.figure.dpi / 96
    if horizontal:
        (b, c), (t, _) = ax.transData.transform([(base, pos), (tip, pos)])
    else:
        (c, b), (_, t) = ax.transData.transform([(pos, base), (pos, tip)])
    h, r = thick_px * k / 2, min(r_px * k, abs(t - b))
    sgn = 1 if t >= b else -1
    pts = [(b, c - h), (t - sgn * r, c - h), (t, c - h), (t, c - h + r), (t, c + h - r), (t, c + h), (t - sgn * r, c + h), (b, c + h), (b, c - h)]
    if not horizontal:
        pts = [(y, x) for x, y in pts]
    codes = [MplPath.MOVETO, MplPath.LINETO, MplPath.CURVE3, MplPath.CURVE3, MplPath.LINETO, MplPath.CURVE3, MplPath.CURVE3,
             MplPath.LINETO, MplPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MplPath(pts, codes), facecolor=color, edgecolor="none", transform=IdentityTransform(), zorder=3))


def save(fig, name):
    fig.savefig(FIG / name, dpi=DPI, facecolor=SURFACE)
    plt.close(fig)


def charts(ch, dev, lp, wk, camp) -> None:
    # 1. Channels: share of sessions against share of sign-ups (dumbbell, one hue, two shades)
    d = ch.sort_values("session_share_pct").reset_index(drop=True)
    hgt = 92 + 64 + 44 * len(d)
    fig, ax = new_fig(hgt, left=0.19)
    ax.set_xlim(0, 40)
    ax.set_ylim(-0.6, len(d) - 0.4)
    ax.set_xticks(range(0, 41, 10), [f"{v}%" for v in range(0, 41, 10)])
    ax.set_yticks(range(len(d)), d["channel_group"], color=INK, fontsize=12.5 * PX)
    ax.grid(axis="x", color=GRID, linewidth=1 * PX, zorder=0)
    for i, r in d.iterrows():
        ax.plot([r["session_share_pct"], r["signup_share_pct"]], [i, i], color=AXIS, linewidth=2 * PX, zorder=2, solid_capstyle="round")
        ax.plot(r["session_share_pct"], i, "o", ms=10 * PX, color=BLUE_LIGHT, mec=SURFACE, mew=2 * PX, zorder=3)
        ax.plot(r["signup_share_pct"], i, "o", ms=10 * PX, color=BLUE_DARK, mec=SURFACE, mew=2 * PX, zorder=4)
        if r["channel_group"] in ("Paid Social", "Direct"):
            lo, hi = sorted([r["session_share_pct"], r["signup_share_pct"]])
            ax.annotate(f"{lo:.0f}%", (lo, i), xytext=(-9 * PX, 0), textcoords="offset points", ha="right", va="center", fontsize=12 * PX, color=INK2)
            ax.annotate(f"{hi:.0f}%", (hi, i), xytext=(9 * PX, 0), textcoords="offset points", ha="left", va="center", fontsize=12 * PX, color=INK2)
    handles = [plt.Line2D([], [], marker="o", ls="", ms=10 * PX, color=BLUE_LIGHT, label="Share of sessions"),
               plt.Line2D([], [], marker="o", ls="", ms=10 * PX, color=BLUE_DARK, label="Share of sign-ups")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.03, 1 - 66 / hgt), ncol=2, frameon=False, fontsize=12 * PX,
               labelcolor=INK2, handletextpad=0.3, columnspacing=1.6, borderaxespad=0, borderpad=0)
    titles(fig, "Paid social brings a third of the traffic and under a fifth of the sign-ups",
           "Each channel's share of sessions and of completed sign-ups", hgt)
    save(fig, "01_channel_share_sessions_vs_signups.png")

    # 2. Funnel step rates, mobile against desktop (two categorical series)
    steps = [("begin_rate_pct", "Started the form\n(of sessions)"), ("otp_rate_pct", "Verified phone\n(of those who started)"),
             ("completion_rate_pct", "Completed sign-up\n(of those verified)")]
    m, k = dev.set_index("device_category").loc["mobile"], dev.set_index("device_category").loc["desktop"]
    hgt = 420
    fig, ax = new_fig(hgt, left=0.08, top_px=104, bottom_px=84)
    ax.set_xlim(-0.6, 2.6)
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 25), [f"{v}%" for v in range(0, 101, 25)])
    ax.set_xticks(range(3), [lab for _, lab in steps], color=INK, fontsize=12.5 * PX)
    ax.grid(axis="y", color=GRID, linewidth=1 * PX, zorder=0)
    ax.axhline(0, color=AXIS, linewidth=1 * PX, zorder=1)
    off = (22 / 2 + 1) / (0.88 * 880) * 3.2          # half a 22px bar plus half the 2px gap, in x units
    for i, (col, _) in enumerate(steps):
        bar(ax, 0, m[col], i - off, BLUE, horizontal=False, thick_px=22)
        bar(ax, 0, k[col], i + off, ORANGE, horizontal=False, thick_px=22)
    for x, v in ((2 - off, m["completion_rate_pct"]), (2 + off, k["completion_rate_pct"])):
        ax.annotate(f"{v:.0f}%", (x, v), xytext=(0, 5 * PX), textcoords="offset points", ha="center", va="bottom", fontsize=12 * PX, color=INK2)
    handles = [plt.Line2D([], [], marker="s", ls="", ms=10 * PX, color=BLUE, label="Mobile"),
               plt.Line2D([], [], marker="s", ls="", ms=10 * PX, color=ORANGE, label="Desktop")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.03, 1 - 66 / hgt), ncol=2, frameon=False, fontsize=12 * PX,
               labelcolor=INK2, handletextpad=0.3, columnspacing=1.6, borderaxespad=0, borderpad=0)
    titles(fig, "Mobile visitors get through OTP as often as desktop, then drop out at the last step",
           "Share of visitors passing each step of the sign-up funnel, by device", hgt)
    save(fig, "02_funnel_steps_mobile_vs_desktop.png")

    # 3. Landing pages ranked by conversion (emphasis: one page is the story)
    d = lp.sort_values("conversion_pct").reset_index(drop=True)
    hgt = 92 + 56 + 34 * len(d)
    fig, ax = new_fig(hgt, left=0.40, bottom_px=56)
    ax.set_xlim(0, 26)
    ax.set_ylim(-0.6, len(d) - 0.4)
    ax.set_xticks([])
    ax.set_yticks(range(len(d)), [f"{p}   {n:,} sessions" for p, n in zip(d["landing_page"], d["sessions"])], color=INK, fontsize=12 * PX)
    ax.axvline(0, color=AXIS, linewidth=1 * PX, zorder=1)
    for i, r in d.iterrows():
        bar(ax, 0, r["conversion_pct"], i, BLUE if r["landing_page"] == "/promo/cashback" else CONTEXT)
        ax.annotate(f"{r['conversion_pct']:.1f}%", (r["conversion_pct"], i), xytext=(7 * PX, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=12 * PX, color=INK if r["landing_page"] == "/promo/cashback" else INK2)
    titles(fig, "The cashback promo page converts at under a tenth of the site average",
           "Sign-up conversion (completed sign-ups / sessions) by landing page", hgt)
    save(fig, "03_landing_page_conversion.png")

    # 4. OTP verification rate by week, iOS against Android (emphasis line)
    hgt = 420
    fig, ax = new_fig(hgt, left=0.08, right=0.90, top_px=104)
    weeks = sorted(wk["week_start"].unique())
    x = {w: i for i, w in enumerate(weeks)}
    ax.set_xlim(-0.4, len(weeks) - 0.6)
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 25), [f"{v}%" for v in range(0, 101, 25)])
    ax.set_xticks(range(0, len(weeks), 2), [pd.Timestamp(w).strftime("%d %b").lstrip("0") for w in weeks[::2]])
    ax.grid(axis="y", color=GRID, linewidth=1 * PX, zorder=0)
    ax.axhline(0, color=AXIS, linewidth=1 * PX, zorder=1)
    ax.axvspan(x["2026-05-18"] - 0.5, x["2026-05-25"] + 0.5, color=BLUE, alpha=0.08, linewidth=0, zorder=0)
    ax.text(x["2026-05-18"] + 0.5, 96, "iOS OTP fault\n18 to 29 May", ha="center", va="top", fontsize=11.5 * PX, color=INK2, linespacing=1.3)
    ends = {}
    for os_name, color, z in (("Android", MUTED, 2), ("iOS", BLUE, 3)):
        g = wk[wk["operating_system"] == os_name]
        xs, ys = [x[w] for w in g["week_start"]], list(g["otp_rate_pct"])
        ax.plot(xs, ys, color=color, linewidth=2 * PX, solid_capstyle="round", solid_joinstyle="round", zorder=z)
        ax.plot(xs[-1], ys[-1], "o", ms=9 * PX, color=color, mec=SURFACE, mew=2 * PX, zorder=z + 2)
        ends[os_name] = (xs[-1], ys[-1])
    upper = max(ends, key=lambda name: ends[name][1])          # the two lines end close together: one label sits just
    for os_name, (xe, ye) in ends.items():                     # above its dot and the other just below, so they never collide
        ax.annotate(f"{os_name} {ye:.0f}%", (xe, ye), xytext=(9 * PX, (1 if os_name == upper else -1) * 3 * PX),
                    textcoords="offset points", ha="left", va="bottom" if os_name == upper else "top", fontsize=12 * PX, color=INK2)
    low = wk[(wk["operating_system"] == "iOS")].sort_values("otp_rate_pct").iloc[0]
    ax.plot(x[low["week_start"]], low["otp_rate_pct"], "o", ms=9 * PX, color=BLUE, mec=SURFACE, mew=2 * PX, zorder=5)
    ax.annotate(f"{low['otp_rate_pct']:.0f}%", (x[low["week_start"]], low["otp_rate_pct"]), xytext=(0, -9 * PX), textcoords="offset points",
                ha="center", va="top", fontsize=12 * PX, color=INK2)
    handles = [plt.Line2D([], [], color=BLUE, lw=2 * PX, label="iOS"), plt.Line2D([], [], color=MUTED, lw=2 * PX, label="Android")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.03, 1 - 66 / hgt), ncol=2, frameon=False, fontsize=12 * PX,
               labelcolor=INK2, handletextpad=0.5, columnspacing=1.6, borderaxespad=0, borderpad=0)
    titles(fig, "For twelve days in May, most iOS users could not verify their phone number",
           "Weekly OTP verification rate (verified / started the form), visitors in Ghana, by operating system", hgt)
    save(fig, "04_otp_rate_weekly_ios_vs_android.png")

    # 5. Cost per sign-up by campaign (ranked bars, one hue)
    d = camp.sort_values("cost_per_signup").reset_index(drop=True)
    hgt = 92 + 56 + 34 * len(d)
    fig, ax = new_fig(hgt, left=0.36, bottom_px=56)
    ax.set_xlim(0, d["cost_per_signup"].max() * 1.18)
    ax.set_ylim(-0.6, len(d) - 0.4)
    ax.set_xticks([])
    ax.set_yticks(range(len(d)), d["campaign"], color=INK, fontsize=12 * PX)
    ax.axvline(0, color=AXIS, linewidth=1 * PX, zorder=1)
    for i, r in d.iterrows():
        bar(ax, 0, r["cost_per_signup"], i, BLUE)
        ax.annotate(f"GHS {r['cost_per_signup']:.0f}", (r["cost_per_signup"], i), xytext=(7 * PX, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=12 * PX, color=INK2)
    worst, second = d.iloc[-1], d.iloc[-2]
    assert worst["campaign"] == "TT_Spark_CashbackChallenge" and worst["cost_per_signup"] > 2 * second["cost_per_signup"]
    titles(fig, f"TikTok's cashback campaign costs GHS {worst['cost_per_signup']:.0f} per sign-up, more than twice any other campaign",
           "Ad cost per completed sign-up (last-click), by campaign", hgt)
    save(fig, "05_cost_per_signup_by_campaign.png")


if __name__ == "__main__":
    main()
