from itertools import combinations


def get_partitions(original_set):
    assert len(original_set) >= 2, "Set cannot be partitioned."

    partitions = []
    for i in range(1, len(original_set) // 2 + 1):
        for subset1_tuple in combinations(original_set, i):
            subset1 = set(subset1_tuple)
            subset2 = original_set - subset1

            if subset1 and subset2:
                partition_pair = tuple(
                    sorted((subset1, subset2), key=lambda x: sorted(list(x)))
                )
                if partition_pair not in partitions:
                    partitions.append(partition_pair)
    return partitions


my_set = {0, 1, 2, 3, 4, 5, 6}
all_partitions = get_partitions(my_set)

for partition in all_partitions:
    print(partition)

print(len(all_partitions))
