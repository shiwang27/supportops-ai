from rag import answer_question


EVALUATION_CASES = (
    {
        "question": "How can a customer reset a forgotten password?",
        "expected_terms": ("password reset", "sign-in page"),
    },
    {
        "question": "What should support ask for when sign-in still fails?",
        "expected_terms": ("account email", "error message"),
    },
)


def run_evaluation():
    case_results = []

    for case in EVALUATION_CASES:
        response = answer_question(case["question"])
        answer = response.answer.lower()
        passed = all(term in answer for term in case["expected_terms"])

        case_results.append(
            {
                "question": case["question"],
                "passed": passed,
                "sources": response.sources,
            }
        )

    passed_count = sum(result["passed"] for result in case_results)
    total_count = len(case_results)

    return {
        "passed": passed_count,
        "total": total_count,
        "accuracy": passed_count / total_count if total_count else 0,
        "cases": case_results,
    }
