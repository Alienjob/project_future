from flask import Blueprint, request, jsonify, render_template
from brownie import network, project, accounts
import os

blockchain_bp = Blueprint('blockchain', __name__)

# Set the path to your Brownie project
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'blockchain'))

# Load the Brownie project
p = project.load(project_path)
p.load_config()
SimpleStorage = p.SimpleStorage

@blockchain_bp.route('/test-storage', methods=['GET', 'POST'])
def test_storage():
    # Connect to the network if not already connected
    if not network.is_connected():
        network.connect('development')

    # Deploy the contract if it's not already deployed
    if len(SimpleStorage) == 0:
        SimpleStorage.deploy({"from": accounts[0]})
    
    contract = SimpleStorage[-1]  # Get the most recently deployed contract

    if request.method == 'GET':
        current_value = contract.get()
        return render_template('test_storage.html', current_value=current_value)
    
    elif request.method == 'POST':
        data = request.json
        if 'value' not in data:
            return jsonify({"error": "No value provided"}), 400
        
        try:
            contract.set(data['value'], {"from": accounts[0]})
            return jsonify({"message": "Value set successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

