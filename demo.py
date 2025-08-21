from neurocache import MemoryModule
import os

# --- 1. Initialize and Remember ---
print("Initializing MemoryModule...")
memory = MemoryModule()
memory.clear() # Start with a clean slate for the demo

print("Remembering two facts...")
memory.remember(key="user_name", value="Himanshu")
memory.remember(key="favorite_food", value="pizza")
print("Done.")

# --- 2. Recall a fact ---
print("\nRecalling user's name...")
user_name = memory.recall(key="user_name")
print(f"  > Recalled name: {user_name}")

# --- 3. Prove Persistence ---
print("\nClosing the script and 'forgetting' the memory object...")
memory.close()
del memory

print("Re-initializing a NEW MemoryModule instance...")
new_memory_instance = MemoryModule()

print("Recalling user's name again (should work)...")
user_name_from_persistence = new_memory_instance.recall(key="user_name")
print(f"  > Recalled name from new instance: {user_name_from_persistence}")
assert user_name_from_persistence == "Himanshu"
print("Persistence test PASSED.")

# --- 4. Clean up ---
print("\nClearing all memories...")
new_memory_instance.clear()
final_recall = new_memory_instance.recall(key="user_name")
print(f"  > Recall after clear: {final_recall}")
assert final_recall is None
print("Clear test PASSED.")

new_memory_instance.close()

# Clean up the database file
if os.path.exists("neurocache.db"):
    os.remove("neurocache.db")
    print("\nCleaned up demo database file.")