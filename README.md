# encryption-demo
## dual custody asymmetric homomorphic encryption

### to use

To give the demo:
```
docker compose run demo
```

To vote, run:
```
docker run -it frankinaustin/dev-sync-demo:latest
```

### requirements and parameters

* Alice and Bob are adversarial. They do not trust each other. They must be able to verify the results.
* Alice and Bob can cooperate when it's in their interest, such as having a fair election.
  * This condition does not supersede the first condition. They *never* trust each other.
* Voters require that they can verify their vote is counted.
* Voters require that their vote is private and can not be recovered.
* The person conducting the poll can not read the results without both Bob and Alice's permission
* The person conducting the poll can tally the votes without Bob and Alice's involvement/permission.
  * These two conditions interact. The person conducting the poll must be able to acquire the results but at the same time must not be able to know the results.