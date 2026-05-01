from pykeen.pipeline import pipeline

result = pipeline(
    model='TransE',
    dataset='nations',
)

print(result.metric_results.to_df())