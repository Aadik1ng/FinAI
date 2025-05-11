import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from src.scenario.pyesg_wrapper import EconomicScenarioGenerator
from src.scenario.scenario_utils import analyze_scenarios, visualize_scenarios, compare_scenarios
from src.knowledge_graph.news_ingestor import FinancialNewsParser
from src.knowledge_graph.graph_builder import KnowledgeGraphBuilder
from src.knowledge_graph.kg_utils import get_entity_relationships, get_temporal_relationships

def demonstrate_scenario_analysis():
    print("\n=== Scenario Analysis Demonstration ===")
    
    # Initialize generator
    generator = EconomicScenarioGenerator()
    
    # Generate scenarios with different models
    gaussian_scenarios = generator.generate_scenarios(
        model_type='gaussian',
        params={'mean': 0.03, 'std': 0.015, 'correlation': 0.4},
        num_scenarios=100
    )
    
    student_t_scenarios = generator.generate_scenarios(
        model_type='student_t',
        params={'mean': 0.03, 'std': 0.015, 'degrees_of_freedom': 5},
        num_scenarios=100
    )
    
    # Analyze scenarios
    print("\nGaussian Model Metrics:")
    gaussian_metrics = analyze_scenarios(gaussian_scenarios)
    print("Mean:", gaussian_metrics['mean'])
    print("Standard Deviation:", gaussian_metrics['std'])
    print("Percentiles:", gaussian_metrics['percentiles'])
    
    print("\nStudent's t Model Metrics:")
    student_t_metrics = analyze_scenarios(student_t_scenarios)
    print("Mean:", student_t_metrics['mean'])
    print("Standard Deviation:", student_t_metrics['std'])
    print("Percentiles:", student_t_metrics['percentiles'])
    
    # Compare scenarios
    scenario_sets = {
        'Gaussian': gaussian_scenarios,
        'Student-t': student_t_scenarios
    }
    comparison = compare_scenarios(scenario_sets)
    print("\nModel Comparison:")
    print(comparison)
    
    # Visualize scenarios
    fig1 = visualize_scenarios(gaussian_scenarios, title="Gaussian Economic Scenarios")
    fig1.savefig('gaussian_scenarios.png')
    plt.close(fig1)
    
    fig2 = visualize_scenarios(student_t_scenarios, title="Student-t Economic Scenarios")
    fig2.savefig('student_t_scenarios.png')
    plt.close(fig2)

def demonstrate_knowledge_graph():
    print("\n=== Knowledge Graph Demonstration ===")
    
    # Initialize components
    news_parser = FinancialNewsParser()
    graph_builder = KnowledgeGraphBuilder()
    
    # Sample financial news articles
    articles = [
        """
        Apple Inc. announced today that it has acquired an AI startup Acme AI for $500 million.
        The deal will help Apple enhance its machine learning capabilities.
        The startup's CEO, John Smith, will join Apple's AI research team.
        """,
        """
        Tesla Motors has partnered with Panasonic to build a new battery factory.
        The partnership aims to increase production capacity by 50%.
        Elon Musk, Tesla's CEO, expects the factory to be operational by 2024.
        """
    ]
    
    # Process articles and build knowledge graph
    all_triples = []
    for article in articles:
        result = news_parser.process_article(article)
        print("\nProcessed Article:")
        print("Entities found:", result['entities'])
        print("Summary:", result['summary'])
        all_triples.extend(result['triples'])
    
    # Build knowledge graph
    graph = graph_builder.build_graph(all_triples)
    
    # Query relationships for specific entities
    apple_entity = "http://example.org/finance/Apple_Inc"
    tesla_entity = "http://example.org/finance/Tesla_Motors"
    
    print("\nApple Inc. Relationships:")
    apple_rels = get_entity_relationships(graph, apple_entity)
    print("Outgoing:", apple_rels['outgoing'])
    print("Incoming:", apple_rels['incoming'])
    
    print("\nTesla Motors Relationships:")
    tesla_rels = get_entity_relationships(graph, tesla_entity)
    print("Outgoing:", tesla_rels['outgoing'])
    print("Incoming:", tesla_rels['incoming'])
    
    # Get temporal relationships
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=1)
    temporal_rels = get_temporal_relationships(graph, start_date, end_date)
    
    print("\nTemporal Relationships (Last 24 hours):")
    for rel in temporal_rels:
        print(f"{rel['subject']} -> {rel['predicate']} -> {rel['object']}")
    
    # Export graph visualization data
    graph_json = graph_builder.export_to_json()
    print("\nKnowledge Graph Structure:")
    print(f"Number of nodes: {len(graph_json['nodes'])}")
    print(f"Number of edges: {len(graph_json['edges'])}")

if __name__ == "__main__":
    demonstrate_scenario_analysis()
    demonstrate_knowledge_graph() 