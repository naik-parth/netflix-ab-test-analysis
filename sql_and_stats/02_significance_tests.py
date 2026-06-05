import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind

print("==================================================")
print(" NETFLIX EXPERIMENT: STATISTICAL SIGNIFICANCE REPORT")
print("==================================================\n")

df = pd.read_csv('netflix_ab_test_logs.csv')

group_a = df[df['test_group'] == 'A (Control)']
group_b = df[df['test_group'] == 'B (Treatment)']

# Test 1: Play Conversion Rate (Chi-Square)
contingency_play = pd.crosstab(df['test_group'], df['clicked_play'])
chi2_play, p_play, _, _ = chi2_contingency(contingency_play)

print("1. PLAY CONVERSION RATE (Chi-Square Test)")
print(f"   P-Value: {p_play:.6f}")
print("   Result:  STATISTICALLY SIGNIFICANT" if p_play < 0.05 else "   Result:  NOT SIGNIFICANT")
print()

# Test 2: Bounce Rate Friction (Chi-Square)
contingency_bounce = pd.crosstab(df['test_group'], df['is_bounce'])
chi2_bounce, p_bounce, _, _ = chi2_contingency(contingency_bounce)

print("2. BOUNCE RATE (Chi-Square Test)")
print(f"   P-Value: {p_bounce:.6f}")
print("   Result:  STATISTICALLY SIGNIFICANT" if p_bounce < 0.05 else "   Result:  NOT SIGNIFICANT")
print()

# Test 3: Average Watch Time (Welch's T-Test)
watch_a = group_a[group_a['is_bounce'] == 0]['total_watch_time_mins']
watch_b = group_b[group_b['is_bounce'] == 0]['total_watch_time_mins']

t_stat, p_watch = ttest_ind(watch_a, watch_b, equal_var=False)

print("3. AVERAGE WATCH TIME (Welch's T-Test)")
print(f"   P-Value: {p_watch:.6f}")
print("   Result:  STATISTICALLY SIGNIFICANT" if p_watch < 0.05 else "   Result:  NOT SIGNIFICANT")
print("\n==================================================")