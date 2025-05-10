class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # use dictionary
        sum_dict = {}

        for i in range(len(nums)):
            num = nums[i]
            if sum_dict.get(target - num) is not None:
                return [sum_dict[target - num], i]
            sum_dict[num] = i
        
