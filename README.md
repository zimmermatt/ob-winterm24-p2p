# Code repository for the Oberlin College Computer Science 2024 Winter Term p2p Software Application Project

## Running
- Source `set-up-python-venv.sh`
- Run `make`

For example:
```sh
. set-up-python-venv.sh
make
```

This will initialize a python environment and activate it locally to this project. To tear down the
environment execute the `deactivate` command at your shell prompt.

## Project Description
[Oberlin College Winter Term 2024 - CS p2p Software Application Project](https://docs.google.com/document/d/1LJIaPwrzWI7uD7HXgcMKWXvHvR8LnMeX44ySQmlCWe4)

### Application Description and Feature Set
- Peer-to-peer Collaborative Art Generator where peers contribute Art Fragments to a drawing
  asynchronously in response to a Commission.
- An Originator Artist (peer) announces a Commission for an Art Piece to create with constraints
  (e.g., color palette, limit to geometric shapes, limit to abstract shapes, etc).
- For the MVP implementation, the application will generate simple Art Fragments. It is not an AI generative art
  application. Though, pluggable generation _may_ be considered.

### Personas

#### Originator Artist
- Commissions and contributes to Collaborative Art Pieces.

#### Contributor Artist
- Contributes to Collaborative Art Pieces.

#### Art Collector
- Collects and trades Art Pieces.
- Commissions Remix Art based on Art Pieces in their Collection.

### User Stories
- As an Originator Artist, I can Commission a new Art Piece, specifying constraints and a deadline,
  so that Contributors can provide Art Fragments.
- As an Originator Artist, I can sign the completed Art Piece I commissioned, so that it can be
  verified as the original.
- As a Contributor artist, I can receive Commission announcements, so that I can contribute Art
  Fragments that I generate.
- As a Contributor artist, I can integrate Art Fragments from other Contributor Artists, so that my
  local canvas reflects the current state of the Art Piece.
- As an Art Collector, I can trade Art Pieces that I own for Art Pieces others own, so that I can vary my art collection.
- As an Art Collector, I can Commission an Art Piece to enhance, so that I can make Remix Art.

### Implementation Notes
- Integration of Art Fragment Contributions will be executed throughout the peers in a decentralized fashion.

## Enhancement List
- May try https://pypi.org/project/nose/ for running tests for its enhanced feature set. The simple
  `Makefile` using `unittest`'s test discovery feature suffices to start.

## References

### Papers
We read and discussed the following papers to serve as input and inspiration for the application
specified above.

- [Kademlia](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf)
- [Kademlia (pre-proceedings paper)](https://www.scs.stanford.edu/~dm/home/papers/kpos.pdf)
- [S/Kademlia](https://citeseerx.ist.psu.edu/pdf/1cc3f1d8e1d7baae2a4b276fbd7bde13afe81f79)
- [Merkle-CRDTs](https://hector.link/presentations/merkle-crdts/merkle-crdts.pdf)
- [IPFS](https://arxiv.org/pdf/1407.3561.pdf)
- [Design and Evaluation of IPFS](https://gipplab.org/wp-content/papercite-data/pdf/trautwein2022a.pdf)
- [Secure Scuttlebutt](https://dl.acm.org/doi/pdf/10.1145/3357150.3357396)
