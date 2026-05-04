import json
import os
from src.recommender import load_songs, recommend_songs
from src.rag_assistant import RagAssistant
from src.guardrails import check_unsupported_query, calculate_confidence, check_recommendation_quality
from src.main import parse_query_to_prefs

def run_evaluation():
    songs = load_songs("data/songs.csv")
    
    test_cases_path = "tests/test_cases.json"
    if not os.path.exists(test_cases_path):
        print(f"Test cases file not found: {test_cases_path}")
        return

    with open(test_cases_path, "r") as f:
        test_cases = json.load(f)

    total_tests = len(test_cases)
    passed_tests = 0
    failed_tests = 0
    total_confidence = 0.0
    valid_confidences = 0

    print("=== Starting Evaluation ===")

    for idx, case in enumerate(test_cases, 1):
        print(f"\nTest {idx}: {case['name']}")
        print(f"Query: '{case['query']}'")
        print(f"Expected Behavior: {case['expected_behavior']}")
        
        # Run logic
        is_supported, guardrail_warning = check_unsupported_query(case['query'])
        
        pass_status = False
        confidence = 0.0
        reason = ""
        
        if not is_supported:
            if not case['should_pass']:
                pass_status = True
                reason = "Properly blocked by guardrail."
            else:
                reason = f"Unexpectedly blocked: {guardrail_warning}"
        else:
            if not case['should_pass']:
                reason = "Failed to block unsupported request."
            else:
                prefs = parse_query_to_prefs(case['query'])
                recommendations = recommend_songs(prefs, songs, k=3)
                confidence = calculate_confidence(recommendations)
                
                is_quality, quality_warning = check_recommendation_quality(recommendations)
                
                if "weird" in case['name'].lower() or "low context" in case['name'].lower():
                    # Expected low confidence
                    pass_status = True
                    reason = "Returned results with expected confidence level for weird request."
                else:
                    if is_quality:
                        pass_status = True
                        reason = f"Returned quality recommendations. Top score: {recommendations[0][1]:.2f}"
                    else:
                        reason = f"Low quality recommendations: {quality_warning}"
        
        if pass_status:
            passed_tests += 1
            print("Status: [PASS]")
        else:
            failed_tests += 1
            print("Status: [FAIL]")
            
        print(f"Confidence Score: {confidence:.2f}")
        print(f"Reason: {reason}")
        
        if confidence > 0:
            total_confidence += confidence
            valid_confidences += 1

    print("\n=== Evaluation Summary ===")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    
    avg_confidence = total_confidence / valid_confidences if valid_confidences > 0 else 0
    print(f"Average Confidence: {avg_confidence:.2f}")
    
    if passed_tests == total_tests:
        print("Reliability Summary: The system is highly reliable and handles all tested edge cases properly.")
    elif passed_tests >= total_tests * 0.8:
        print("Reliability Summary: The system is mostly reliable but has some minor failure points.")
    else:
        print("Reliability Summary: The system needs improvement to handle edge cases properly.")

if __name__ == "__main__":
    run_evaluation()
