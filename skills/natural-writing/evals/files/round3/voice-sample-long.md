# Search migration: voice sample and draft

## Voice sample

Okay. Search. Let's do search, because I have been living in it for three weeks and I have opinions now.

The thing I keep coming back to is that we never needed Elasticsearch. Not really. We needed *a* search box — one — and somebody back in 2019 (not me, though I signed off on it, so, equally guilty) picked the thing everyone picks. Then we paid for it every month for five years. Twelve nodes. Twelve! For a corpus of forty million documents that barely changes from one week to the next.

The gnarly part isn't the money — the money was annoying but survivable. The gnarly part is that nobody left on the team could tell you how any of it worked. Analyzers, tokenizers, a mapping file nobody dared touch (there is a comment in it that just says "do not remove", unsigned, undated, which is either a joke or a threat). We had a search system and zero search engineers — that is the actual bill, and it is not the one on the invoice.

So: Postgres. Same database we already run, already back up, already know how to restore at four in the morning.

Was it a downgrade? Yeah, a bit. Lucene is genuinely better at this than Postgres is — I am not going to pretend otherwise, and anyone who tells you tsvector is a drop-in replacement for a real search engine is selling you something. But better at what, exactly. Our queries are short. Two words, three words. Nobody here is doing fuzzy phrase matching across a legal corpus — they are typing "blue mug" and expecting the blue mug.

The migration itself was boring, which is the highest compliment I hand out. Build the GIN index (nine hours, ran it on a replica, nobody noticed). Dual-write for a week — cheap, boring, worth it. Compare the top twenty results for the thousand most common queries, eyeball the diffs, fix the ranking weights twice (twice! I was braced for twenty). Cut over on a Wednesday morning, because Wednesday mornings are quiet and because I wanted to be awake for it.

Latency got worse. Saying it out loud: worse. Not gnarly-worse — just worse, and I would do it again, because the p95 that actually matters is the one on the day the search cluster is having a bad day, and now there is no search cluster to have one.

Three weeks. One index. Twelve fewer nodes to patch (and one fewer dashboard I have to pretend to read). Anyway — that is the whole story, and if you are sitting on a search cluster nobody understands (you know if you are), the gnarly truth is you already know what I am going to tell you.

## Draft

This document describes the migration of the product search index from Elasticsearch to PostgreSQL full-text search. The migration was completed over a period of three weeks and is now fully deployed in production.

The Elasticsearch cluster was originally provisioned in 2019 to support product search across the catalog. At the time of the migration, the cluster consisted of 12 nodes and indexed approximately 40 million documents. The monthly infrastructure cost of the cluster was approximately $4,000. The document corpus is relatively static, with a low rate of change from one week to the next.

Several factors motivated the decision to migrate. The first factor was cost. The second factor was operational knowledge. No members of the current engineering team had significant experience with Elasticsearch configuration, including analyzers, tokenizers, and the index mapping file. This created a situation in which the search system was difficult to modify safely and difficult to reason about during incidents. The third factor was operational overhead, as the cluster required patching and capacity management that was not otherwise necessary.

PostgreSQL, referred to internally as Postgres, was selected as the replacement because it was already in use as the primary datastore. Existing backup, restore, and monitoring procedures already covered the database, which meant that no new operational procedures were required.

It should be acknowledged that PostgreSQL full-text search is less capable than Lucene, which is the engine underlying Elasticsearch. However, an analysis of production query logs indicated that the majority of user queries consist of two or three terms. Advanced capabilities such as fuzzy phrase matching across large text corpora were not observed in meaningful volume. The reduced capability was therefore assessed as an acceptable tradeoff.

The migration was carried out in four phases. In the first phase, a GIN index was built over a tsvector column covering the product title and description fields. The index build took nine hours and was performed on a read replica in order to avoid impact to production traffic. In the second phase, writes were sent to both systems for a period of one week to allow the new index to reach consistency with the existing one. In the third phase, result quality was validated by comparing the top 20 results returned by each system for the 1,000 most frequent production queries. Discrepancies were reviewed and the ranking weights applied by ts_rank were adjusted on two occasions. In the fourth phase, the cutover was performed on a Wednesday morning, a period selected because query volume is historically low at that time.

Latency results were mixed. Prior to the migration, p95 search latency was 180 ms. Following the migration, p95 search latency was 240 ms, representing an increase of approximately 33 percent. This regression was accepted for two reasons. First, the absolute latency remains within the product requirement of 500 ms. Second, the elimination of the Elasticsearch cluster removes an entire class of availability incidents in which search latency degraded substantially during cluster events.

The outcome of the migration can be summarized as follows. Monthly infrastructure cost was reduced by approximately $4,000. The number of nodes requiring patching and monitoring was reduced by 12. The search implementation is now expressed in SQL, which every engineer on the team is able to read and modify. Median latency increased modestly and remains within requirements.

Several items remain outstanding. Synonym handling is currently implemented through a static dictionary and will need to be revisited if the catalog expands into new categories. Multilingual support is not currently implemented and would require additional configuration of text search dictionaries. Finally, index maintenance procedures should be documented, as GIN index bloat has not yet been observed but is expected over a longer time horizon. A runbook entry covering index rebuild and the expected duration of that operation on the replica should be added before the next quarter, and ownership of that runbook should be assigned to a named engineer rather than to the team as a whole.

Teams considering a similar migration should evaluate their own query distribution before assuming that the tradeoff described here applies to their situation. The decision was appropriate for a small corpus of short queries and would likely not be appropriate for a search product where relevance quality is the primary differentiator.
