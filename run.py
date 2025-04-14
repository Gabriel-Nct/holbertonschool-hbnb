import os
from app import create_app
from app.services.facade import HBnBFacade

flask_env = os.getenv('FLASK_ENV', 'development')
config_mapping = {
    'development': 'development',
    'testing': 'testing',
    'production': 'production'
}
config_class = config_mapping.get(flask_env, 'development')
app = create_app(config_class)

if __name__ == '__main__':
    if app.config['DEBUG']:
        facade = HBnBFacade()
        try:
            test_user = facade.get_user_by_email('test@example.com')
            if not test_user:
                user_data = {
                    'first_name': 'Test',
                    'last_name': 'User',
                    'email': 'test@example.com',
                    'password': 'testpassword'
                }
                test_user = facade.create_user(user_data)
                print(f"✅ Test user created: {test_user.to_dict()}")
            else:
                print(f"ℹ️ Test user already exists: {test_user.to_dict()}")
        except Exception as e:
            print(f"❌ Error creating test user: {e}")

    app.run(debug=True)
