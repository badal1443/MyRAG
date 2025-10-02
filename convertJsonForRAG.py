import json
import csv
from datetime import datetime

def prepare_jira_data_for_rag(jira_json_file, output_csv_file):
    """
    Convert JIRA JSON data to RAG-friendly CSV format
    """
    
    # Load your JIRA JSON data
    with open(jira_json_file, 'r', encoding='utf-8') as f:
        jira_data = json.load(f)
    
    # Prepare data for RAG
    rag_documents = []
    
    for ticket in jira_data:
        # Create a comprehensive text chunk for each ticket
        content_parts = [
            f"Ticket ID: {ticket['key']}",
            f"Type: {ticket['issueType']}",
            f"Summary: {ticket['summary']}",
            f"Description: {ticket['description']}",
            f"Status: {ticket['status']}",
            f"Fix Version: {ticket['fixVersion']}",
            f"Production Release Date: {ticket['productionReleaseDate']}"
        ]
        
        # Add comments if they exist
        if ticket.get('comments'):
            content_parts.append("Comments:")
            for comment in ticket['comments']:
                content_parts.append(f"- {comment['author']} ({comment['date']}): {comment['text']}")
        
        # Combine all parts
        full_content = "\n".join(content_parts)
        
        # Create metadata for filtering and search
        metadata = {
            "ticket_id": ticket['key'],
            "issue_type": ticket['issueType'],
            "status": ticket['status'],
            "fix_version": ticket['fixVersion'],
            "release_date": ticket['productionReleaseDate'],
            "summary": ticket['summary']
        }
        
        rag_documents.append({
            "id": ticket['key'],
            "content": full_content,
            "title": f"{ticket['key']}: {ticket['summary']}",
            "metadata": json.dumps(metadata),
            #"url": f"https://yourjira.atlassian.net/browse/{ticket['key']}"  # Adjust to your JIRA URL
        })
    
    # Save to CSV format (Azure AI Search friendly)
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'content', 'title', 'metadata', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for doc in rag_documents:
            writer.writerow(doc)
    
    print(f"Prepared {len(rag_documents)} documents for RAG")
    print(f"Output saved to: {output_csv_file}")
    
    return rag_documents

# Example usage:
# rag_docs = prepare_jira_data_for_rag('jira_data.json', 'jira_rag_data.csv')

# Alternative: Create individual text files (another option for upload)
def create_individual_files(jira_json_file, output_directory):
    """
    Create individual .txt files for each JIRA ticket
    """
    import os
    
    with open(jira_json_file, 'r', encoding='utf-8') as f:
        jira_data = json.load(f)
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for ticket in jira_data:
        filename = f"{ticket['key']}.txt"
        filepath = os.path.join(output_directory, filename)
        
        content = f"""JIRA Ticket: {ticket['key']}
Type: {ticket['issueType']}
Summary: {ticket['summary']}
Status: {ticket['status']}
Fix Version: {ticket['fixVersion']}
Release Date: {ticket['productionReleaseDate']}

Description:
{ticket['description']}

Comments:
"""
        
        if ticket.get('comments'):
            for comment in ticket['comments']:
                content += f"- {comment['author']} ({comment['date']}): {comment['text']}\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"Created {len(jira_data)} individual text files in {output_directory}")

# Example usage:
# create_individual_files('jira_data.json', 'jira_documents/')

if __name__ == "__main__":
    # Run the conversion
    prepare_jira_data_for_rag('rde_jira_sample_data.json', 'jira_rag_data.csv')
    #create_individual_files('jira_data.json', 'jira_documents/')