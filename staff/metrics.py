from collections import defaultdict

class AnalysisCalculator:
    """Utility class for calculating analysis metrics"""
    
    @staticmethod
    def process_feedback(feed_dict):
        """Process a single feedback dictionary"""
        if not isinstance(feed_dict, dict):
            return []
        
        processed_data = []
        for cat_num, value in feed_dict.items():
            if isinstance(value, (int, float)):
                processed_data.append({
                    f'{cat_num}': value
                })
        return processed_data

    @staticmethod
    def compute_metrics(data, terms):
        if not data:
            return {
                "category_averages": {},
                "counts": {},
                "percentages": {},
                "category_percentages": {},
                "terms": terms
            }

        # Initialize counters
        category_sums = defaultdict(float)
        category_counts = defaultdict(int)
        score_counts = defaultdict(int)
        total_items = 0

        # Process the data
        for item in data:
            for cat, value in item.items():
                category_sums[cat] += value
                category_counts[cat] += 1
                score_counts[value] += 1
                total_items += 1

        # Calculate metrics
        category_averages = {
            cat: round(sum_val / category_counts[cat], 2)
            for cat, sum_val in category_sums.items()
        }

        counts = {
            score: count
            for score, count in score_counts.items()
            if score in [1, 3, 5]
        }

        percentages = {
            score: round((count / total_items) * 100, 2)
            for score, count in counts.items()
        }

        category_percentages = {
            cat: round((sum_val / (category_counts[cat] * 5)) * 100, 2)
            for cat, sum_val in category_sums.items()
        }

        return {
            "category_averages": category_averages,
            "counts": counts,
            "percentages": percentages,
            "category_percentages": category_percentages,
            "terms": terms
        }


class DeptAnalysisCalculator:
    """Utility class for calculating analysis metrics"""
    
    @staticmethod
    def process_feedback(feed_dict):
        """Process a single feedback dictionary"""
        if not isinstance(feed_dict, dict):
            return []
        
        processed_data = []
        for cat_num, value in feed_dict.items():
            if isinstance(value, (int, float)):
                processed_data.append({
                    f'{cat_num}': value
                })
        return processed_data

    @staticmethod
    def compute_metrics(data, terms):
        if not data:
            return {
                "category_averages": {},
                "counts": {},
                "percentages": {},
                "category_percentages": {},
                "terms": terms
            }

        # Initialize counters
        category_sums = defaultdict(float)
        category_counts = defaultdict(int)
        score_counts = defaultdict(int)
        total_items = 0

        # Process the data
        for item in data:
            for cat, value in item.items():
                if cat != 'dept':  # Skip the dept field
                    category_sums[cat] += value
                    category_counts[cat] += 1
                    score_counts[value] += 1
                    total_items += 1

        # Calculate metrics
        category_averages = {
            cat: round(sum_val / category_counts[cat], 2)
            for cat, sum_val in category_sums.items()
        }

        counts = {
            score: count
            for score, count in score_counts.items()
            if score in [1, 3, 5]
        }

        percentages = {
            score: round((count / total_items) * 100, 2)
            for score, count in counts.items()
        }

        category_percentages = {
            cat: round((sum_val / (category_counts[cat] * 5)) * 100, 2)
            for cat, sum_val in category_sums.items()
        }

        return {
            "category_averages": category_averages,
            "counts": counts,
            "percentages": percentages,
            "category_percentages": category_percentages,
            "terms": terms
        }
class ReportMetricsCalculator:
    ''' utitly class for report data '''
    @staticmethod
    def _process_feedback_dict(feed_dict):
        """Process a single feedback dictionary and extract values"""
        if not isinstance(feed_dict, dict):
            return []
        return list(feed_dict.values())

    @staticmethod
    def _compute_metrics(data):
        """Compute percentage metrics for a series of values"""
        total = len(data)
        if total == 0:
            return {
                "percentage_5s": 0,
                "percentage_3s": 0,
                "percentage_1s": 0,
                "average": 0
            }
        
        counts = defaultdict(int)
        sum_values = 0
        
        for value in data:
            counts[value] += 1
            sum_values += value
            
        return {
            "percentage_5s": round((counts[5] / total) * 100, 2),
            "percentage_3s": round((counts[3] / total) * 100, 2),
            "percentage_1s": round((counts[1] / total) * 100, 2),
            "average": round(sum_values / total, 2)
        }

class FeedbackMetricsCalculator:
    """Utility class for calculating feedback metrics"""
    
    @staticmethod
    def compute_metrics(scores):
        """Compute percentage metrics for a series of values"""
        if not scores:
            return {
                "5s": 0,
                "3s": 0,
                "1s": 0,
                "avg": 0
            }
        
        total = len(scores)
        counts = defaultdict(int)
        total_sum = 0
        
        for score in scores:
            counts[score] += 1
            total_sum += score
            
        return {
            "5s": round((counts[5] / total) * 100, 2),
            "3s": round((counts[3] / total) * 100, 2),
            "1s": round((counts[1] / total) * 100, 2),
            "avg": round(total_sum / total, 2)
        }

    @staticmethod
    def process_feedback(feed_dict):
        """Process a single feedback dictionary"""
        if not isinstance(feed_dict, dict):
            return []
        return [val for val in feed_dict.values() if isinstance(val, (int, float))]
